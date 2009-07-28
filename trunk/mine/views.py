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

def REST(request, *args, **kwargs):
    get_view = kwargs.pop('GET', None)
    post_view = kwargs.pop('POST', None)
    delete_view = kwargs.pop('DELETE', None)

    if request.method == 'GET' and get_view is not None:
        return get_view(request, *args, **kwargs)
    elif request.method == 'POST' and post_view is not None:
        return post_view(request, *args, **kwargs)
    elif request.method == 'DELETE' and delete_view is not None:
        return delete_view(request, *args, **kwargs)

    raise Http404

##################################################################

## url: /
## method: read_mine_root
## args:
def read_mine_root(request, *args, **kwargs):
    raise Http404('method read_mine_root for url / is not yet implemented')

## url: /api
## method: read_api_root
## args:
def read_api_root(request, *args, **kwargs):
    raise Http404('method read_api_root for url /api is not yet implemented')

## url: /doc
## method: read_doc
## args:
def read_doc(request, *args, **kwargs):
    raise Http404('method read_doc for url /doc is not yet implemented')

## url: /get
## method: read_minekey
## args:
def read_minekey(request, *args, **kwargs):
    raise Http404('method read_minekey for url /get is not yet implemented')

## url: /get
## method: create_minekey
## args:
def create_minekey(request, *args, **kwargs):
    raise Http404('method create_minekey for url /get is not yet implemented')

## url: /pub
## method: read_pub
## args:
def read_pub(request, *args, **kwargs):
    raise Http404('method read_pub for url /pub is not yet implemented')

## url: /ui
## method: read_ui_root
## args:
def read_ui_root(request, *args, **kwargs):
    raise Http404('method read_ui_root for url /ui is not yet implemented')
