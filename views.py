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

from api.models import LogEvent

import django.utils.simplejson as json
import pickle

def REST(request, *args, **kwargs):

    """Things that use REST() return their own HTTPResponse objects
    directly; this includes item-data-reads, and most non-API
    handlers"""

    el = LogEvent.open("REST",
                       ip=request.META['REMOTE_ADDR'],
                       method=request.method,
                       path=request.path,
                       )

    get_view = kwargs.pop('GET', None)
    post_view = kwargs.pop('POST', None)
    delete_view = kwargs.pop('DELETE', None)

    response = None

    if request.method == 'GET' and get_view is not None:
        response = get_view(request, *args, **kwargs)
    elif request.method == 'POST' and post_view is not None:
        response = post_view(request, *args, **kwargs)
    elif request.method == 'DELETE' and delete_view is not None:
        response = delete_view(request, *args, **kwargs)
    else:
        el.close_error('oops')
        raise Http404, "cannot find handler for REST request method"

    el.close()
    return response

def API_CALL(request, *args, **kwargs):

    """
    Things that use API_CALL() return a structure that here is
    converted to the desired output format and returned.

    The pseudo-format "api" enables use of the redirect_success
    parameter; if "foo.api" is called and "redirect_success" is set,
    then a successful completion of foo.api yields a redirect to the
    value of "redirect_success"
    """

    el = LogEvent.open("API",
                       ip=request.META['REMOTE_ADDR'],
                       method=request.method,
                       path=request.path,
                       )

    get_view = kwargs.pop('GET', None)
    post_view = kwargs.pop('POST', None)
    delete_view = kwargs.pop('DELETE', None)
    desired_format = kwargs.pop('fmt', None)

    if desired_format == 'api' and \
            'redirect_success' not in request.REQUEST:
        raise RuntimeError, "'api' format requested and redirect_success not set"

    retval = None

    if request.method == 'GET' and get_view is not None:
        retval = get_view(request, *args, **kwargs)
    elif request.method == 'POST' and post_view is not None:
        retval = post_view(request, *args, **kwargs)
    elif request.method == 'DELETE' and delete_view is not None:
        retval = delete_view(request, *args, **kwargs)
    else:
        raise Http404, "cannot find handler for API_CALL request method"

    if not retval:
        raise RuntimeError, "received None as return value from API_CALL request method"

    data = None
    mimetype = None

    # how to deal with / format the results
    if desired_format == 'api':
        dest = request.REQUEST['redirect_success']
        return HttpResponseRedirect(dest) # fast 302 redirect to page
    elif desired_format == 'json':
        mimetype="application/json"
        data = json.dumps(retval)
    elif desired_format == 'xml':
        mimetype="application/xml"
        data = None
        raise RuntimeError("XML serialization disabled temporarily due to lack of 'lxml' on OSX")
    elif desired_format == 'py':
        mimetype="text/plain"
        data = pickle.dumps(retval)

    # else it plain worked
    el.close()
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

