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
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404

import pymine.api.views as api
from pymine.api.models import Tag, Item, Relation, Comment, VanityURL

from minekey import MineKey

##################################################################

## rest: GET /get
## function: root_get
## declared args: 
def root_get(request, *args, **kwargs):
    return render_to_response('root-get.html')

## rest: GET /get/KEY
## function: read_minekey
## declared args: key
def read_minekey(request, key, *args, **kwargs):

    # parse it out (basic validation performed)
    mk = MineKey.parse(key)

    # check get vs put
    if mk.method != "get":
        raise RuntimeError, "minekey is not 'get' method: " + str(mk)

    # check depth
    if mk.depth <= 0:
        raise RuntimeError, "minekey has run out of depth: " + str(mk)

    # check global ToD restrictions
    # TODO

    # load relation
    try:
        r = Relation.objects.get(id=mk.rid)
    except Relation.DoesNotExist, e:
        raise RuntimeError, "minekey rid is not valid: " + str(mk)

    # check rvsn
    if r.version != mk.rvsn:
        raise RuntimeError, "minekey rvsn / relation version mismatch: " + str(mk)

    # check against relation IP address
    if r.network_pattern:
        if 'REMOTE_ADDR' not in request.META:
            raise RuntimeError, "relation specifies network pattern but REMOTE_ADDR unavailable: " + str(r)

        src = request.META.get('REMOTE_ADDR')

        # this is hardly CIDR but can be fixed later
        if not src.startswith(r.network_pattern):
            raise RuntimeError, "relation being accessed from illegal REMOTE_ADDR: " + src

    # check ToD against relation embargo time
    # TODO

    # deal with it
    if mk.iid: # is an actual item
        return api.read_item_data(None, mk.iid)
    else: # is a feed
        return HttpResponse("feed decoded: " + str(mk))


## rest: POST /get/KEY
## function: submit_minekey
## declared args: key
def submit_minekey(request, key, *args, **kwargs):
    s = {}
    return render_to_response('submit-minekey.html', s)

