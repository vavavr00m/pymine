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

class create_feedqs(request, feed):
    return Item.list()

class render_feedqs_with_minekey(request, qs, mk):

    feed_info = {}
    feed_info['author_email'] = 'nobody-feed@themineproject.org'
    feed_info['author_link'] = None
    feed_info['author_name'] = feed_info['author_email']
    feed_info['categories'] = None
    feed_info['feed_copyright'] = None
    feed_info['feed_guid'] = None
    feed_info['feed_url'] = mk.permalink()
    feed_info['language'] = None
    feed_info['link'] = mk.permalink()
    feed_info['subtitle'] = None
    feed_info['title'] = '%s feed' % feed.name
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

    # populate with respect to the minekey
    feed = feedgenerator.Atom1Feed(**feed_info)

    for i in qs:
	item_info = i.to_atom(mk, feed)
	feed.add_item(**item_info)

    return HttpResponse(feed.writeString('UTF-8'), mimetype='application/atom+xml')
