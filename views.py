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

    """Things that use REST() return their own HTTPResponse objects
    directly; this includes item-data-reads, and most non-API
    handlers"""

    get_view = kwargs.pop('GET', None)
    post_view = kwargs.pop('POST', None)
    delete_view = kwargs.pop('DELETE', None)

    if request.method == 'GET' and get_view is not None:
        return get_view(request, *args, **kwargs)
    elif request.method == 'POST' and post_view is not None:
        return post_view(request, *args, **kwargs)
    elif request.method == 'DELETE' and delete_view is not None:
        return delete_view(request, *args, **kwargs)

    raise Http404, "cannot find handler for REST request method"


def API_CALL(request, *args, **kwargs):

    """Things that use API_CALL() return a structure that here is
    converted to the desired output format and returned; if
    redirect_success is set, that is executed here as well."""

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

    if not retval:
        raise Http404, "cannot find handler for API_CALL request method"

    data = None
    mimetype = None

    if desired_format == 'py':
        mimetype="text/plain"
        data = pickle.dumps(retval)
    elif desired_format == 'json':
        mimetype="application/json"
        data = json.dumps(retval)
    elif desired_format == 'xml':
        mimetype="application/xml"
        data = None
        raise Http404("XML serialization disabled temporarily due to lack of 'lxml' on OSX")

    if not data:
        raise Http404, "received None as return value from API method"

    # if we get here, it worked; are we punting?

    if 'redirect_success' in request.REQUEST:
        dest = request.REQUEST['redirect_success']
        return HttpResponseRedirect(dest)

    # else it plain worked
    return HttpResponse(data, mimetype=mimetype)


##################################################################

## rest: GET /
## function: read_mine_root
## declared args: 
def read_mine_root(request, *args, **kwargs):
    return render_to_response('root-mine.html')

## rest: GET /doc
## function: read_doc_root
## declared args: 
def read_doc_root(request, *args, **kwargs):
    return render_to_response('root-doc.html')

## rest: GET /pub
## function: read_pub_root
## declared args: 
def read_pub_root(request, *args, **kwargs):
    return render_to_response('root-pub.html')

