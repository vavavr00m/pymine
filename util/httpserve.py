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

"""
http://docs.djangoproject.com/en/dev/howto/static-files/ says:

<QUOTE>Django itself doesn't serve static (media) files, such as
images, style sheets, or video. It leaves that job to whichever Web
server you choose.  The reasoning here is that standard Web servers,
such as Apache, lighttpd and Cherokee, are much more fine-tuned at
serving static files than a Web application framework.</QUOTE>

...which is fine, but which doesn't actually help us when Django is
being used to implement potentially hundreds of mini-websites with
their own novel forms of authentication and where you don't want
management overhead of keeping (documenting?) how to synchronise their
authentication needs with [INSERT NAME OF PREFERRED WEBSERVER DU
JOUR].

See also: http://code.djangoproject.com/ticket/2131#comment:2

<QUOTE>Django isn't meant to serve static files, so I'm marking this
as a wontfix.</QUOTE>

So in the face of those wanting to nanny us into "proper behaviour",
regrettably we have to roll our own.

We are allowed to take the performance hit, because the point is to
have "one mine per user spattered all over the world" rather than
"bazillion mines all at one hosting company which subsequently suffers
performance issues".
"""

from django.conf import settings
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.core.servers.basehttp import FileWrapper
from django.shortcuts import render_to_response
import os
import re

##################################################################

mime_table = {
    '.avi': 'video/x-msvideo',
    '.css': 'text/css',
    '.dcr': 'application/x-director',
    '.gif': 'image/gif',
    '.htm': 'text/html',
    '.html': 'text/html',
    '.ico': 'image/vnd.microsoft.icon',
    '.jpeg': 'image/jpeg',
    '.jpg': 'image/jpeg',
    '.js': 'application/javascript',
    '.json': 'application/json',
    '.mov': 'video/quicktime',
    '.pdf': 'application/pdf',
    '.png': 'image/png',
    '.ram': 'audio/x-pn-realaudio',
    '.rm': 'application/vnd.rn-realmedia',
    '.swf': 'application/x-shockwave-flash',
    '.txt': 'text/plain',
}

def mime_lookup(path):
    head, tail = os.path.split(path)
    base, ext = os.path.splitext(tail)
    ext = ext.lower()
    return mime_table.get(ext, 'text/plain')

##################################################################

def cleanpath(old):
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
	elements.pop(-1) # explicit

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

def httpserve_error(url_path):
    return Http404(url_path)

##################################################################

def httpserve_file(file_path, content_type):
    fw = FileWrapper(file(file_path), 65536)
    if not content_type:
	content_type = mime_lookup(file_path)
    response = HttpResponse(fw, content_type=content_type)
    response['Content-Length'] = os.path.getsize(file_path)
    return response

##################################################################

def httpserve_directory(file_path):
    s = {
	'name' : 'insert dirname here',
	'list' : [],
	}

    list = s['list']

    files = os.listdir(file_path)
    files.sort()

    for file in files:
        if file.startswith("."):
            continue
	if os.path.isdir(os.path.join(file_path, file)):
	    list.append(dict(name=file,
			     link='%s/' % file,
			     description='[dir]'))
	else:
	    list.append(dict(name=file,
			     link=file,
			     description=''))

    return render_to_response('list/directory.html', s)

##################################################################

def httpserve_path(request, orig_path):

    # clean the url
    url_path = cleanpath(orig_path)

    # if the cleaning has changed anything, force user to go around again
    if url_path != orig_path:
	redirect_path = "%s/pub/%s" % (settings.MINE_URL_ROOT, url_path)
	return HttpResponseRedirect(redirect_path)

    # if there's a url_path
    if url_path == '':
	# there's no orig_path
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
		return httpserve_file(ifile, None)

	# else raw directory
	return httpserve_directory(file_path)

    # if it's a file
    elif os.path.isfile(file_path):
	return httpserve_file(file_path, None)

    # if it's an other
    return httpserve_error(url_path)

##################################################################
