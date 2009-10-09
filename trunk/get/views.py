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

from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponsePermanentRedirect
from django.shortcuts import render_to_response, get_object_or_404

import pymine.api.views as api
from pymine.api.models import Tag, Item, Relation, Comment, Vurl

from minekey import MineKey

##################################################################
##################################################################
##################################################################

def demofeed(request, *args, **kwargs):

    r = Relation.objects.get(id=1)

    # where X = the union of tag.cloud for each tag in relation.tags
    for rtag in r.tags.all():
	for ctag in rtag.cloud.all():
	    x[ctag] = True

    # the feed comprises:
    # (
    # items marked for:relation
    # so long as they are public or shared
    # +
    # items tagged FOO where FOO is in X
    # so long as they are public
    # )
    # distinct
    # excluding any marked not:relation
    # excluding any matching "except:tag" from relation.excludes
    # excluding any NOT matching "require:tag" from relation.requires
    # excluding any that are currently hidden
    # excluding any that are private ## MUGTRAP
    # sorted by most recently modified

    qs = Item.objects.order_by('-name')

    # dump it as a list
    result = [ item.to_structure() for item in qs ]
    s = { 'result': result,
          'status': 'this is a fake page for demofeed',
          'exit': 0,
          }
    return render_to_response('list-items.html', s)

##################################################################
##################################################################
##################################################################

## rest: GET /get
## function: root_get
## declared args:
def root_get(request, *args, **kwargs):
    s = {}
    return render_to_response('root-get.html', s)

## rest: GET /get/MINEKEY
## function: read_minekey
## declared args: minekey
def read_minekey(request, minekey, *args, **kwargs):
    # log this
    el = LogEvent.open("MKREAD", )

    # big wrapper for all possible exceptions
    try:
	# parse it out (basic validation performed)
	mk = MineKey.parse(minekey)

	# extended validation
	mk.validate_against(request, 'get')

	# deal with it
	if mk.iid: # item
	    retval = api.read_item_data(None, mk.iid)
	    el.close('item processed')
	    return retval
	else: # feed
	    retval = HttpResponse("feed decode: " + str(mk))
	    el.close('feed processed')
	    return retval

    # catch all
    except Exception, e:
	el.close_error(str(e))
	raise

## rest: POST /get/MINEKEY
## function: submit_minekey
## declared args: minekey
def submit_minekey(request, minekey, *args, **kwargs):
    s = {}
    return render_to_response('submit-minekey.html', s)

## rest: GET /get/i/VID
## function: redirect_vid
## declared args: vid
def redirect_vid(request, vid, *args, **kwargs):
    v = Vurl.objects.get(id=int(vid))
    return HttpResponsePermanentRedirect(v.link.strip()) # issue 301 redirect

## rest: GET /get/r/VURLKEY
## function: redirect_vurlkey
## declared args: vurlkey
def redirect_vurlkey(request, vurlkey, *args, **kwargs):
    v = Vurl.get_with_vurlkey(vurlkey.encode('utf-8'))
    return HttpResponsePermanentRedirect(v.link.strip()) # issue 301 redirect

## rest: GET /get/v/SUFFIX
## function: redirect_vurlname
## declared args: suffix
def redirect_vurlname(request, suffix, *args, **kwargs):
    v = Vurl.objects.get(name=suffix)
    return HttpResponsePermanentRedirect(v.link.strip()) # issue 301 redirect

