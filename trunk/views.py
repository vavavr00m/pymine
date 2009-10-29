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

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404

import django.utils.simplejson as json
import pickle

from api.models import LogEvent

import util.cheatxml as cheatxml
import util.httpserve as httpserve

##################################################################

def REST_NOAUTH(request, *args, **kwargs):

    """Things that use REST()/REST_NOAUTH() return their own HTTPResponse
    objects directly; this includes item-data-reads, and most non-API
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

    if ((request.method == 'DELETE') or
	(request.method == 'POST' and
	 request.REQUEST.get('_method', None) == 'DELETE')) and \
	delete_view is not None:
	response = delete_view(request, *args, **kwargs)
    elif request.method == 'POST' and post_view is not None:
	response = post_view(request, *args, **kwargs)
    elif request.method == 'GET' and get_view is not None:
	response = get_view(request, *args, **kwargs)
    else:
	el.close_error('oops')
	raise Http404, "cannot find handler for REST request method"

    el.close()
    return response


##################################################################

@login_required()
def REST(request, *args, **kwargs):
    """ frontend to REST_NOAUTH() but uses the @login_required decorator"""
    return REST_NOAUTH(request, *args, **kwargs)

##################################################################

@login_required
def API_CALL(request, *args, **kwargs):
    """
    Things that use API_CALL() return a structure that here is
    converted to the desired output format and returned.

    The pseudo-format "rdr" enables use of the redirect_success
    parameter; if "foo.rdr" is called and "redirect_success" is set,
    then a successful completion of foo.rdr yields a redirect to the
    value of "redirect_success"

    The format "raw" returns a undefined string representation of the
    results for "foo.raw", purely for human consumption.  If DEBUG is
    set then the return value is type text/plain, otherwise it is
    application/octet-stream.
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

    if desired_format == 'rdr' and \
	    'redirect_success' not in request.REQUEST:
	raise RuntimeError, "rdr (redirect) format requested and redirect_success not set"

    retval = None

    if ((request.method == 'DELETE') or
	(request.method == 'POST' and
	 request.REQUEST.get('_method', None) == 'DELETE')) and \
	delete_view is not None:
	retval = delete_view(request, *args, **kwargs)
    elif request.method == 'POST' and post_view is not None:
	retval = post_view(request, *args, **kwargs)
    elif request.method == 'GET' and get_view is not None:
	retval = get_view(request, *args, **kwargs)
    else:
	raise Http404, "cannot find handler for API_CALL request method"

    if not retval:
	raise RuntimeError, "received None as return value from API_CALL request method"

    data = None
    mimetype = None

    # how to deal with / format the results
    if desired_format == 'rdr':
	dest = request.REQUEST['redirect_success']
	return HttpResponseRedirect(dest) # fast 302 redirect to page
    elif desired_format == 'raw':
	if settings.DEBUG:
	    mimetype="text/plain" # so we can see what's going on
	else:
	    mimetype="application/octet-stream"
	data = str(retval.get('result', ''))
    elif desired_format == 'xml':
	mimetype="application/xml"
	data = cheatxml.dumps(retval)
    elif desired_format == 'json':
	mimetype="application/json"
	data = json.dumps(retval, sort_keys=True, indent=2)
    elif desired_format == 'py':
	mimetype="text/plain"
	data = pickle.dumps(retval)

    # else it plain worked
    el.close()
    return HttpResponse(data, mimetype=mimetype)

##################################################################

## rest: GET /
## function: root_mine
## declared args: 
def root_mine(request, *args, **kwargs):
    """root_mine() returns ..."""
    s = {}
    return render_to_response('dash/root.html', s)

## rest: GET /favicon.ico
## function: root_favicon
## declared args: 
def root_favicon(request, *args, **kwargs):
    """root_favicon() returns ..."""
    return handle_pub(request, 'images/favicon.ico', *args, **kwargs)

## rest: GET /pub/
## function: root_pub
## declared args: 
def root_pub(request, *args, **kwargs):
    """root_pub() returns ..."""
    return handle_pub(request, '', *args, **kwargs)

## rest: GET /pub/SUFFIX
## function: handle_pub
## declared args: suffix
def handle_pub(request, suffix, *args, **kwargs):
    """handle_pub(suffix) returns ..."""
    return httpserve.httpserve_path(request, suffix)

