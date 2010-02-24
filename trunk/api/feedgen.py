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

#from datetime import datetime
from django.conf import settings
#from django.core.urlresolvers import reverse
#from django.db.models import Q
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils import feedgenerator

from pymine.api.models import Item # Tag, Feed, Comment, Vurl

#import django.utils.simplejson as json
#import pickle

"""docstring goes here""" # :-)

def generate_feed(feedmk):
    """
    wrapper for combined render_feedqs and create_feedqs
    """

    return render_feedqs(feedmk, create_feedqs(feedmk))

def create_feedqs(feedmk):
    """
    create a queryset giving all the items pertinent to be served to feedmk
    """

    return Item.list()

def render_feedqs(feedmk, qs):
    """
    take a feedmk and a (presumably pertinent) queryset, and generate ATOM for the former using the latter.
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

    fgen = feedgenerator.Atom1Feed(**feed_info)

    for i in qs:
	item_info = i.to_atom(feedmk)
	fgen.add_item(**item_info)

    return HttpResponse(fgen.writeString('UTF-8'), mimetype='application/atom+xml')
