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

from django.conf import settings
from django.core.servers.basehttp import FileWrapper
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404

import django.utils.simplejson as json
import os
import pickle
import re

from api.models import LogEvent

import cheatxml.cheatxml as cheatxml

##################################################################

mime_table = {
    '.css': 'text/css',
    '.gif': 'image/gif',
    '.htm': 'text/html',
    '.html': 'text/html',
    '.jpeg': 'image/jpeg',
    '.jpg': 'image/jpeg',
    '.pdf': 'application/pdf',
    '.png': 'image/png',
    '.txt': 'text/plain',
}

def mime_lookup(path):
    head, tail = os.path.split(path)
    base, ext = os.path.splitext(tail)
    ext = ext.lower()
    return mime_table.get(ext, 'text/plain')

def http_serve_file(file_path, content_type):
    fw = FileWrapper(file(file_path), 65536)
    if not content_type:
        content_type = mime_lookup(file_path)
    response = HttpResponse(fw, content_type=content_type)
    response['Content-Length'] = os.path.getsize(file_path)
    return response

def http_serve_directory(file_path):
    s = { 
        'name' : 'insert dirname here',
        'list' : [],
        }

    list = s['list']

    files = os.listdir(file_path)
    files.sort()

    for file in files:
        if os.path.isdir(os.path.join(file_path, file)):
            list.append(dict(name=file, 
                             link='%s/' % file, 
                             description='[dir]'))
        else:
            list.append(dict(name=file, 
                             link=file, 
                             description=''))

    return render_to_response('directory-listing.html', s)

def http_serve_error(url_path):
    raise Exception, 'file not found: %s' % url_path # TBD: make 404 !!!!!!!!!!!!!!!!

##################################################################

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

def clean_url_path(old):
    # fasttrack root
    if not old or (old == '/'):
	return ''

    # fault anything with a "?" - we don't do those
    if old.find('?') >= 0:
	raise RuntimeError, "string contains query data: %s" % old

    # is there a trailing slash?
    if old.endswith('/'):
	has_trailing = True
    else:
	has_trailing = False

    # split on slash/multislash
    elements = re.split('/+', old)

    if not elements: return ''

    # delete any trailing empty element
    if elements[-1] == '':
	elements.pop(-1)

    if not elements: return ''

    # delete any element which is "."
    elements = [ x for x in elements if x != '.' ]

    if not elements: return ''

    # for any element which is "..", delete it and its previous
    output = []
    while elements:
	x = elements.pop(0)
	if x == '..':
	    if output:
		output.pop()
	else:
	    output.append(x)
    elements = output

    if not elements: return ''

    # result
    new = "/".join(elements)

    # reappend trailing slash
    if has_trailing:
	new += '/'

    # join
    return new

##################################################################

## rest: GET /
## function: root_mine
## declared args:
def root_mine(request, *args, **kwargs):
    """
    This method renders 'root-mine.html' which provides a HTML
    response for requests to the mine's root URL.
    """

    s = {}
    return render_to_response('root-mine.html', s)

## rest: GET /pub/
## function: root_pub
## declared args:
def root_pub(request, *args, **kwargs):
    """
    handles the root of the public_html directory
    """
    return handle_pub(request, '', *args, **kwargs)

## rest: GET /pub/SUFFIX
## function: handle_pub
## declared args: suffix
def handle_pub(request, suffix, *args, **kwargs):
    """
    http://docs.djangoproject.com/en/dev/howto/static-files/ says:

    <QUOTE>Django itself doesn't serve static (media) files, such as
    images, style sheets, or video. It leaves that job to whichever
    Web server you choose.  The reasoning here is that standard Web
    servers, such as Apache, lighttpd and Cherokee, are much more
    fine-tuned at serving static files than a Web application
    framework.</QUOTE>

    ...which is fine, but which doesn't actually help us when Django
    is being used to implement potentially hundreds of mini-websites
    with their own novel forms of authentication and where you don't
    want management overhead of keeping (documenting?) how to
    synchronise their authentication needs with [INSERT NAME OF
    PREFERRED WEBSERVER DU JOUR].

    See also: http://code.djangoproject.com/ticket/2131#comment:2

    <QUOTE>Django isn't meant to serve static files, so I'm marking
    this as a wontfix.</QUOTE>

    So in the face of those wanting to nanny us into "proper
    behaviour", regrettably we have to roll our own.

    We are allowed to take the performance hit, because the point is
    to have "one mine per user spattered all over the world" rather
    than "bazillion mines all at one hosting company which
    subsequently suffers performance issues".
    """

    # clean the url
    url_path = clean_url_path(suffix)

    # if the cleaning has changed anything, force user to go around again
    if url_path != suffix:
	redirect_path = "%s/pub/%s" % (settings.MINE_URL_ROOT, url_path)
	return HttpResponseRedirect(redirect_path)

    # if there's a url_path
    if url_path == '':
	# there's no suffix
	file_path = settings.MEDIA_ROOT
    else:
	# split the url_path into components
	elements = url_path.split('/')

	# compose a file path
	file_path = os.path.join(settings.MEDIA_ROOT, *elements)

    # if it's a directory
    if os.path.isdir(file_path):

	# redirect if a trailing slash is missing
	if not (url_path == '' or url_path.endswith('/')):
	    redirect_path = "%s/pub/%s/" % (settings.MINE_URL_ROOT, url_path)
	    return HttpResponseRedirect(redirect_path)

	# look for an index
	for i in ('index.html', 'index.htm', 'INDEX.HTML', 'INDEX.HTM'):
	    ifile = os.path.join(file_path, i)
	    if os.path.isfile(ifile):
		return http_serve_file(ifile, None)

	# else raw directory
	return http_serve_directory(file_path)

    # if it's a file
    elif os.path.isfile(file_path):
	return http_serve_file(file_path, None)

    # if it's an other
    return http_serve_error(url_path)
