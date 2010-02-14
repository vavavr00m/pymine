#!/usr/bin/python
##
## Copyright 2009-2010 Adriana Lukas & Alec Muffett
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

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, HttpResponseNotAllowed, HttpResponsePermanentRedirect
from django.shortcuts import render_to_response

from api.models import Vurl

import django.utils.simplejson as json
import pickle

import util.cheatxml as cheatxml
import util.httpserve as httpserve

def HTTP_METHOD_NOAUTH(request, *args, **kwargs):
    """
    deal with a non-API HTTP request : GET and POST methods
    """

    if request.method == 'POST':
	viewlist = kwargs.pop('POST', None)
    elif request.method == 'GET':
	viewlist = kwargs.pop('GET', None)

    # viewlist should now be [ method, defarg ... ]
    if not viewlist:
	 return HttpResponseNotAllowed([ x for x in kwargs.keys() if x in ('GET', 'POST') ])

    # purposely drop *args on the floor - we don't know where it's been
    view = viewlist[0]
    viewargs = viewlist[1:]
    return view(request, *viewargs, **kwargs)

@login_required
def HTTP_METHOD(request, *args, **kwargs):
    """frontend to HTTP_METHOD_NOAUTH but uses the @login_required decorator"""
    return HTTP_METHOD_NOAUTH(request, *args, **kwargs)

@login_required
def API_REST(request, *args, **kwargs):
    """
    deal with an API HTTP request : GET, POST and DELETE methods
    """

    if ((request.method == 'DELETE') or
	(request.method == 'POST' and request.POST.get('_method', None) == 'DELETE')):
	viewlist = kwargs.pop('DELETE', None)
    elif request.method == 'POST':
	viewlist = kwargs.pop('POST', None)
    elif request.method == 'GET':
	viewlist = kwargs.pop('GET', None)

    desired_format = kwargs.pop('fmt', None)

    if desired_format == 'rdr' and 'redirect_success' not in request.REQUEST:
	return HttpResponseForbidden('redirection url used but "redirect_success" not set')

    if desired_format not in ('json', 'xml', 'rdr', 'txt'):
	return HttpResponseForbidden('illegal output format')

    if not viewlist:
	 return HttpResponseNotAllowed([ x for x in kwargs.keys() if x in ('GET', 'POST', 'DELETE') ])

    # purposely drop *args on the floor - we don't know where it's been
    view = viewlist[0]
    viewargs = viewlist[1:]

    # API calls give us an response envelope / structure; we have to format it
    # print 'args', args
    # print 'viewargs', viewargs
    # print 'kwargs', kwargs
    envelope = view(request, *viewargs, **kwargs)

    # coersce to the output format
    if desired_format == 'json':
	mimetype = "application/json"
	data = json.dumps(envelope, sort_keys=True, indent=2)
    elif desired_format == 'xml':
	mimetype = "application/xml"
	data = cheatxml.dumps(envelope)
    elif desired_format == 'txt':
	mimetype = "text/plain"
	data = cheatxml.dumps(envelope) # same as XML, just text/plain content-type
    elif desired_format == 'rdr':
	dest = request.REQUEST['redirect_success']
	return HttpResponseRedirect(dest) # fast 302 redirect to page
    else:
	HttpResponseForbidden("this can't happen")

    # return the result
    return HttpResponse(data, mimetype=mimetype)

##################################################################

# this definition (get_favicon) is auto-generated.
# ensure that any changes are made via the generator.
def get_favicon(request, **kwargs):
    """
    arguments: request, **kwargs
    implements: GET /favicon.ico
    returns: a punt to mine_public(request, 'images/favicon.ico', **kwargs)
    """
    return mine_public(request, 'images/favicon.ico', **kwargs)

##################################################################

# this definition (mine_public) is auto-generated.
# ensure that any changes are made via the generator.
def mine_public(request, suffix, **kwargs):
    """
    arguments: request, suffix, **kwargs
    implements: GET /pub(/SUFFIX)
    returns: the output of httpserve.httpserve_path(request, suffix)
    """
    return httpserve.httpserve_path(request, suffix)

##################################################################

# this definition (mine_redirect) is auto-generated.
# ensure that any changes are made via the generator.
def mine_redirect(request, target, **kwargs):
    """
    arguments: request, target, **kwargs
    implements: GET /
    returns: HttpResponseRedirect(target)
    """
    return HttpResponseRedirect(target)

##################################################################

# this definition (minekey_read) is auto-generated.
# ensure that any changes are made via the generator.
def minekey_read(request, mk_hmac, mk_fid, mk_fversion, mk_iid, mk_depth, mk_type, mk_ext, **kwargs):
    """
    arguments: request, mk_hmac, mk_fid, mk_fversion, mk_iid, mk_depth, mk_type, mk_ext, **kwargs
    implements: GET /key/(MK_HMAC)/(MK_FID)/(MK_FVERSION)/(MK_IID)/(MK_DEPTH)/(MK_TYPE).(MK_EXT)
    returns: ...
    """
    pass

##################################################################

# this definition (minekey_submit) is auto-generated.
# ensure that any changes are made via the generator.
def minekey_submit(request, mk_hmac, mk_fid, mk_fversion, mk_iid, mk_depth, mk_type, mk_ext, **kwargs):
    """
    arguments: request, mk_hmac, mk_fid, mk_fversion, mk_iid, mk_depth, mk_type, mk_ext, **kwargs
    implements: POST /key/(MK_HMAC)/(MK_FID)/(MK_FVERSION)/(MK_IID)/(MK_DEPTH)/(MK_TYPE).(MK_EXT)
    returns: ...
    """
    pass

##################################################################

# this definition (vurl_read_by_key) is auto-generated.
# ensure that any changes are made via the generator.
def vurl_read_by_key(request, vurlkey, **kwargs):
    """
    arguments: request, vurlkey, **kwargs
    implements: GET /vurl/(VURLKEY)
    returns: vurl.http_response()
    """
    v = Vurl.get_with_vurlkey(vurlkey.encode('utf-8'))
    return v.http_response()

##################################################################

# this definition (vurl_read_by_name) is auto-generated.
# ensure that any changes are made via the generator.
def vurl_read_by_name(request, suffix, **kwargs):
    """
    arguments: request, suffix, **kwargs
    implements: GET /page/(SUFFIX)
    returns: vurl.http_response()
    """
    v = Vurl.objects.get(name=suffix)
    return v.http_response()

##################################################################
