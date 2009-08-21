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

import django.utils.simplejson as json
import pickle

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

    raise Http404, "fell off the end of REST"

def API_CALL(request, *args, **kwargs):
    get_view = kwargs.pop('GET', None)
    post_view = kwargs.pop('POST', None)
    delete_view = kwargs.pop('DELETE', None)
    desired_format = kwargs.pop('fmt', None)

    retval = None

    if request.method == 'GET' and get_view is not None:
        retval = get_view(request, *args, **kwargs)
    elif request.method == 'POST' and post_view is not None:
        retval = post_view(request, *args, **kwargs)
    elif request.method == 'DELETE' and delete_view is not None:
        retval = delete_view(request, *args, **kwargs)

    if retval:
        if desired_format == 'py':
            data = pickle.dumps(retval)
            return HttpResponse(data, mimetype="text/plain")
        elif desired_format == 'json':
            data = json.dumps(retval)
            return HttpResponse(data, mimetype="application/json")
        elif desired_format == 'xml':
            raise Http404("XML serialization disabled temporarily due to lack of 'lxml' on OSX")
            data = None
            return HttpResponse(data, mimetype="application/xml")

    raise Http404, "fell off the end of API_CALL"

##################################################################

## rest: GET /
## function: read_mine_root
## declared args: 
def read_mine_root(request, *args, **kwargs):
    return render_to_response('read-mine-root.html')

## rest: GET /doc
## function: read_doc_root
## declared args: 
def read_doc_root(request, *args, **kwargs):
    return render_to_response('read-doc-root.html')

## rest: GET /pub
## function: read_pub_root
## declared args: 
def read_pub_root(request, *args, **kwargs):
    return render_to_response('read-pub-root.html')

