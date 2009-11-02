#!/usr/bin/python
##
## Copyright 2009 Adriana Lukas & Alec Muffett
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

"""docstring goes here""" # :-)

from datetime import datetime
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import Http404, HttpResponse, HttpResponsePermanentRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template.loader import render_to_string
from django.utils import feedgenerator

from pymine.api.models import Tag, Item, Relation, Comment, Vurl, LogEvent, Minekey

import pymine.api.views as api

##################################################################
##################################################################
##################################################################

# PRIORITIES:
#
# item.STATUS=PRIVATE trumps...
# item.HIDDEN_TIME trumps...
# not:RELATION trumps...
# [MINEKEY DIRECT ACCESS (PUBLIC|SHARED)>] trumps...
# [FEED] for:RELATION(PUBLIC|SHARED) trumps...
# [FEED] exclude:TAG trumps...
# [FEED] require:TAG trumps...
#...(there could be an argument for moving minekey here)...
# [FEED] intersection of ITEM(PUBLIC).EXPANDEDTAGCLOUD and RELATION.INTERESTS.

def generate_feed(request, mkencoded, *args, **kwargs):

    slicesize = 100

    mk = Minekey.parse(mkencoded)
    rid = mk.rid

    # who are we looking at?
    relation = Relation.objects.select_related(depth=2).get(id=rid)

    # when is it?
    now = datetime.now()

    # what are they interested in, like, and hate?
    interests = relation.interests.all()
    needs = relation.interests_required.all()
    hates = relation.interests_excluded.all()

    # first, deal with the 'interests' - this means public objects.
    # TBD: add a constraint in here that nothing > N days old is
    # considered for the feed?
    public_items = Item.objects.filter(status='P').select_related(depth=2)

    # where we will stash the IIDs of candidate items
    candidates = []

    # for every item get its tag
    # for every tag, get its cloud
    # if relation hates things in the cloud, drop item
    # if relation needs things and any of them are missing, drop item
    # else mark item as candidate

    # print "%s interests %s" % (relation.name, str(interests))
    # print "%s hates %s" % (relation.name, str(hates))
    # print "%s needs %s" % (relation.name, str(needs))

    for item in public_items.all():
	# print "considering %s" % item.name

	for item_tag in item.tags.all():
	    item_cloud = item_tag.cloud.all()

	    # print "examining %s -> %s" % (item_tag, str(item_cloud))

	    if hates:
		if item_cloud & hates: # <-- BITWISE NOT LOGICAL 'AND'
		    # print "avoiding %s because hates %s" % (item.name, str(hates))
		    break

	    if needs:
		obtained = item_cloud.values_list('id', flat=True)
		unobtained = needs.exclude(id__in=obtained)
		if unobtained:
		    # print "avoiding %s because needs %s" % (item.name, str(unobtained))
		    break

	    if item_cloud & interests: # <-- BITWISE NOT LOGICAL 'AND'
		# print "candidate %s" % item.name
		candidates.append(item.id)
		break

    # re-use cached public_items to recreate the proper selection
    qs1 = public_items.filter(id__in=candidates)

    # and rip out those extra "public" or "shared" items explicitly for us
    qs2 = relation.items_explicitly_for.filter(Q(status='P') | Q(status='S'))

    # collate and uniq the above
    qs = qs1 | qs2
    qs = qs.distinct()

    # remove any marked as private (should be none bwtf)
    qs = qs.exclude(status='X')

    # reject items marked not:relation (i wish i could do qs = qs - blacklist)
    blacklist = relation.items_explicitly_not.values_list('id', flat=True)
    qs = qs.exclude(id__in=blacklist)

    # reject items that are currently hidden
    qs = qs.exclude(hide_after__isnull=False, hide_after__lte=now)
    qs = qs.exclude(hide_before__isnull=False, hide_before__gt=now)

    # sort MRF (TBD: artificially promote hidden-but-revealed into sort order)
    qs = qs.order_by('-last_modified')

    # slice it
    qs = qs[:slicesize]

    # feed information
    feedinfo = {}
    feedinfo['author_email'] = None
    feedinfo['author_link'] = None
    feedinfo['author_name'] = None
    feedinfo['categories'] = None
    feedinfo['feed_copyright'] = None
    feedinfo['feed_guid'] = None
    feedinfo['feed_url'] = mk.permalink()
    feedinfo['language'] = None
    feedinfo['link'] = mk.permalink()
    feedinfo['subtitle'] = None
    feedinfo['title'] = 'test feed'
    feedinfo['ttl'] = None

    fd_tmpl = { # not everything/identical
	'author_email': feedinfo['author_email'],
	'author_link': feedinfo['author_link'],
	'author_name': feedinfo['author_name'],
	'feed_copyright': feedinfo['feed_copyright'],
	'feed_url': feedinfo['feed_url'],
	'link': feedinfo['link'],
	'subtitle': feedinfo['subtitle'],
	'title': feedinfo['title'],
	}

    feedinfo['description'] = render_to_string('feed/feed-description.html', fd_tmpl)

    # populate with respect to the minekey
    feed = feedgenerator.Atom1Feed(**feedinfo)

    for item in qs:
	iteminfo = item.to_atom(mk)
	feed.add_item(**iteminfo)

    return HttpResponse(feed.writeString('UTF-8'), mimetype='application/atom+xml')



# TBD TO BE DONE - 

# DOES THE FEED GENERATION BELONG HERE?  SHOULD IT NOT BE SPLIT INTO
# LIST-OF-ITEMS GENERATION *AND* FEED CREATION *AND* RESPONSE?

# MOST IMPORTANTLY: DOES IT USE REPLICATE THE LOGIC OF
# VALIDATE_AGAINST() RE: EMBARGOES, ETC...  CAN WE MERGE/COLLATE THE
# FUNCTIONALITY TO REMOVE REPLICATION?

# SHOULD VALIDATE_AGAINST BECOME VALIDATE_RELATIONSHIP?  

# IS THERE YET NO NOT:RELATION TESTING FOR ITEM FETCHES?

# BREAK SLICESIZE OUT INTO A SETTING?  EVENTUALLY MAKE IT
# SINCE-LAST-ACCESS BASED RETREIVAL?



##################################################################
##################################################################
##################################################################

## rest: GET /get/MINEKEY
## function: read_minekey
## declared args: minekey
def read_minekey(request, minekey, *args, **kwargs):
    """read_minekey(minekey) returns ..."""

    # log this
    el = LogEvent.open("minekey", )

    # big wrapper for all possible exceptions
    try:
	# parse it out (basic validation performed)
	mk = Minekey.parse(minekey)

	# extended validation
	mk.validate_against(request, 'get')

	# deal with it
	if mk.iid: # item
	    retval = api.read_item_data(None, mk.iid, minekey=mk)
	    el.close('item ok')
	    return retval
	else: # feed
	    retval = generate_feed(request, minekey, *args, **kwargs)
	    el.close('feed ok')
	    return retval

    # catch all
    except Exception, e:
	el.close_error(str(e))
	raise






## rest: POST /get/MINEKEY
## function: submit_minekey
## declared args: minekey
def submit_minekey(request, minekey, *args, **kwargs):
    """submit_minekey(minekey) returns ..."""
    s = {}
    return render_to_response('submit/minekey.html', s)






## rest: POST /get/m
## function: field_minekey
## declared args: 
def field_minekey(request, *args, **kwargs):
    """field_minekey() returns ..."""
    # TBD: DELETE THIS COMMENT WHEN THE CODE IS DONE
    s = api.field_minekey(request, *args, **kwargs)
    return render_to_response('field/minekey.html', s)







## rest: GET /get/i/VID
## function: redirect_vid
## declared args: vid
def redirect_vid(request, vid, *args, **kwargs):
    """redirect_vid(vid) looks up the Vurl with index VID and issues a HTTP 301 redirect to the target URL"""
    v = Vurl.objects.get(id=int(vid))
    return HttpResponsePermanentRedirect(v.link) # issue 301 redirect



## rest: GET /get/k/VURLKEY
## function: redirect_vurlkey
## declared args: vurlkey
def redirect_vurlkey(request, vurlkey, *args, **kwargs):
    """redirect_vurlkey(vurlkey) looks up the Vurl with base58-encoded index VURLKEY and issues a HTTP 301 redirect to the target URL"""
    v = Vurl.get_with_vurlkey(vurlkey.encode('utf-8'))
    return HttpResponsePermanentRedirect(v.link) # issue 301 redirect



## rest: GET /get/n/SUFFIX
## function: redirect_vurlname
## declared args: suffix
def redirect_vurlname(request, suffix, *args, **kwargs):
    """redirect_vurlname(suffix) looks up the Vurl with the long pseudo-path SUFFIX and issues a HTTP 301 redirect to the target URL"""
    v = Vurl.objects.get(name=suffix)
    return HttpResponsePermanentRedirect(v.link) # issue 301 redirect
