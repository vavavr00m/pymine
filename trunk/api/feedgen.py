#!/usr/bin/python
##
## Copyright 2010 Adriana Lukas & Alec Muffett
##
## Licensed under the Apache License, Version 2.0 (the "License"); you
## may not use this file except in compliance with the License. You
## may obtain a copy of the License at
##
## http://www.apache.org/licenses/LICENSE-2.0
##
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
## implied. See the License for the specific language governing
## permissions and limitations under the License.
##

from datetime import datetime
#from django.conf import settings
#from django.core.urlresolvers import reverse
from django.db.models import Q
#from django.http import Http404, HttpResponse
#from django.shortcuts import render_to_response, get_object_or_404
#from django.template.loader import render_to_string
#from django.utils import feedgenerator
#from pymine.api.models import Tag, Item, Relation, Comment, Vurl, LogEvent, Minekey
#from pymine.views import API_CALL
#import django.utils.simplejson as json
#import pickle
#import util.cheatxml as cheatxml
#import util.minesearch as minesearch
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils import feedgenerator
from pymine.api.models import Item, Feed

"""docstring goes here""" # :-)

def generate_feed(feedmk):
    """
    wrapper for combined render_feedqs and create_feedqs
    """

    return render_feedqs(feedmk, create_feedqs(feedmk))

def render_feedqs(feedmk, qs):
    """
    take a feedmk and a (presumably pertinent) queryset, and generate FEEDXML for the former using the latter.
    """

    feed = feedmk.get_feed()
    feed_info = {}

    feed_info['author_email'] = 'noreply-feed@localhost'
    feed_info['feed_url'] = feedmk.permalink()
    feed_info['title'] = '%s feed' % feed.name

    feed_info['author_name'] = feed_info['author_email']
    feed_info['link'] = feed_info['feed_url']

    feed_info['author_link'] = None
    feed_info['categories'] = None
    feed_info['feed_copyright'] = None
    feed_info['feed_guid'] = None
    feed_info['language'] = None
    feed_info['subtitle'] = None
    feed_info['ttl'] = None

    fdesc_tmpl = { # not everything/identical
	'author_email': feed_info['author_email'],
	'author_link': feed_info['author_link'],
	'author_name': feed_info['author_name'],
	'feed_copyright': feed_info['feed_copyright'],
	'feed_url': feed_info['feed_url'],
	'link': feed_info['link'],
	'subtitle': feed_info['subtitle'],
	'title': feed_info['title'],
	}

    feed_info['description'] = render_to_string('feedgen/feed-description.html', fdesc_tmpl)

    #fgen = feedgenerator.Atom1Feed(**feed_info)
    fgen = feedgenerator.Rss201rev2Feed(**feed_info)

    if qs:
	for i in qs:
	    item_info = i.to_feedxml(feedmk)
	    fgen.add_item(**item_info)

    #return HttpResponse(fgen.writeString('UTF-8'), mimetype='application/atom+xml')
    return HttpResponse(fgen.writeString('UTF-8'), mimetype='application/rss+xml')

def create_feedqs(feedmk):
    """
    create a queryset giving all the items pertinent to be served to feedmk

    PRIORITIES:
    item.STATUS=PRIVATE trumps...
    item.HIDDEN_TIME trumps...
    not:FEED trumps...
    [MINEKEY DIRECT ACCESS (PUBLIC|SHARED)>] trumps...
    [FEED] for:FEED(PUBLIC|SHARED) trumps...
    [FEED] exclude:TAG trumps...
    [FEED] require:TAG trumps...
    ..(there could be an argument for moving minekey here)...
    [FEED] intersection of ITEM(PUBLIC).EXPANDEDTAGCLOUD and FEED.INTERESTS.
    """

    # maximum amount of stuff we want to generate
    slicesize = 128

    # who are we looking at?
    fid = feedmk.get_feed().id

    # get a fresh copy of the feed, and use select_related; in the
    # future patch this to do the many2many expansion thing...

    feed = Feed.objects.select_related(depth=2).get(id=fid)

    # when is it?

    now = datetime.now()

    # what are they interested-in, need, and hate?

    interests = feed.interests.all()
    needs = feed.interests_require.all()
    hates = feed.interests_exclude.all()
    constraints = feed.content_constraints

    # first, deal with the 'interests' - this means 'shared' objects.

    # TBD: add a constraint in here that nothing > N days old is
    # considered for the feed?

    public_items = Item.list().filter(status='S').select_related(depth=2)
    #print "tagshared items>>", str(public_items.all())

    # where we will stash the IIDs of candidate items
    candidates = []

    # for every item get its tag
    # for every tag, get its cloud
    # if feed hates things in the cloud, drop item
    # if feed needs things and any of them are missing, drop item
    # else mark item as candidate

    # TBD: THIS IS ALL GOING TO GET REWRITTEN AS THE INTERSECTION AND
    # JOINING OF THREE QUERIES AT SOME POINT IN THE FUTURE.

    #print "%s interests %s" % (feed.name, str(interests))
    #print "%s hates %s" % (feed.name, str(hates))
    #print "%s needs %s" % (feed.name, str(needs))

    # small cache to try to prevent unnecessary lookups
    cloud_cache = {}

    for item in public_items.filter(is_deleted__exact=False):
	#print "considering tagshared item %s" % item.name

	for item_tag in item.tags.all():
	    if item_tag in cloud_cache:
		item_cloud = cloud_cache[item_tag]
	    else:
		item_cloud = cloud_cache[item_tag] = item_tag.cloud.all()

	    #print "examining tag: %s -> cloud: %s" % (item_tag, str(item_cloud))
	    if hates:
		if item_cloud & hates: # <-- BITWISE NOT LOGICAL 'AND'
		    #print "avoiding %s because hates %s" % (item.name, str(hates))
		    break

	    if needs:
		obtained = item_cloud.values_list('id', flat=True)
		unobtained = needs.exclude(id__in=obtained)
		if unobtained:
		    #print "avoiding %s because needs %s" % (item.name, str(unobtained))
		    break

	    if item_cloud & interests: # <-- BITWISE NOT LOGICAL 'AND'
		#print "marking candidate %s" % item.name
		candidates.append(item.id)
		break

    # re-use cached public_items to recreate the proper selection
    qs1 = public_items.filter(id__in=candidates)
    #print "shared candidates>>", str(qs1.all())

    # and rip out those extra "citable" or "shared" items explicitly for us
    qs2 = feed.items_explicitly_for.filter( Q(status='C') | Q(status='S') ).filter(is_deleted__exact=False)
    #print "citation candidates>>", str(qs2.all())

    # collate and uniq the above
    qs = qs1 | qs2
    qs = qs.distinct()
    #print "distinct candidates>>", str(qs.all())

    # reject items marked not:feed (i wish i could do qs = qs - blacklist)
    blacklist = feed.items_explicitly_not.values_list('id', flat=True)
    qs = qs.exclude(id__in=blacklist)

    # reject items that are currently hidden
    qs = qs.exclude(hide_after__isnull=False, hide_after__lte=now)
    qs = qs.exclude(hide_before__isnull=False, hide_before__gt=now)

    # sort MRF (TBD: artificially promote hidden-but-revealed into sort order)
    qs = qs.order_by('-last_modified')

    #print "sorted>>", str(qs.all())

    # per-feed constraints
    if False and constraints:
	rules = minesearch.parse(constraints)

	if len(rules['query']):
	    q = Q()
	    for key, value in rules['query']:
		if key == 'token':
		    q = q | Q(name__icontains=value) | Q(description__icontains=value)
		elif key == 'type':
		    q = q | Q(type__iexact=value)
		else:
		    raise RuntimeError, 'do not understand feed query: %s' % key
	    qs = qs.filter(q)

	if len(rules['require']):
	    for key, value in rules['require']:
		if key == 'token':
		    qs = qs.filter(Q(name__icontains=value) | Q(description__icontains=value))
		elif key == 'type':
		    qs = qs.filter(type__iexact=value)
		else:
		    raise RuntimeError, 'do not understand feed requirement: %s' % key

	if len(rules['exclude']):
	    for key, value in rules['exclude']:
		if key == 'token':
		    qs = qs.exclude(Q(name__icontains=value) | Q(description__icontains=value))
		elif key == 'type':
		    qs = qs.exclude(type__iexact=value)
		else:
		    raise RuntimeError, 'do not understand feed exclusion: %s' % key

    # the safety catch
    if feed.is_considered_public:
	qs = qs.filter(is_considered_public=True)

    # pagination goes here
    # foo

    #print "preslice>>", str(qs.all())

    # slice it
    qs = qs[:slicesize]

    # return it
    return qs
