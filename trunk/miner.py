#!/usr/bin/python

##
## Copyright 2009-10 Adriana Lukas & Alec Muffett
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
Miner:

Provides the MineAPI class for client development *and* the
command_line uploader for pymine.  There are essentially two ways to
use Miner; first you instantiate it:

    m = MineAPI(**apiopts)

...and then either you treat it like a client library:

    foo = m.create_item(name="Something")
    print foo
    tags = m.list_tags()

...or you treat it like the command_line interface:

    foo = m.command_line("create-item", "name=Something")
    print foo
    tags = m.command_line("list-tags")

If going down the latter route, don't mess around with the XML-output
options otherwise nothing good will come of it.

If going down the command_line route, the "delete-*" methods implement
a "__FAKE_ITERATION_KLUDGE__" - in other words you can pass multiple
thing IDs into the command_line and they will be serially deleted,
even though the underlying library calls do not take multiple
arguments.  This exists only for the beenfit of actual commandline
(shell) users, and shouldn't be used programmatically since it makes a
nonsense of exception handling.
"""

# essential reading:
# http://stackoverflow.com/questions/407468/python-urllib2-file-upload-problems

from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
from urllib2 import HTTPError

import cookielib
import django.utils.simplejson as simplejson
import getopt
import getpass
import os
import re
import sys
import urllib
import urllib2

# OM NOM NOM NOM NOM
cookie_file = 'etc/cookies2.txt'
cookie_jar = cookielib.LWPCookieJar(cookie_file)
if (os.path.isfile(cookie_file)): cookie_jar.load()
urllib2.install_opener(urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie_jar)))

# register streaming handlers for poster
poster_opener = None # register_openers()

class MineAPI:
    def __init__(self, **kwargs):
	"""
	Initialise a MineAPI object; Recognised kwargs include:

	output_format
	url_prefix
	username
	password

	Automatically calls login() if both username and password are given.
	"""

	self.output_format = kwargs.get('output_format', None)
	self.url_prefix = kwargs.get('url_prefix', 'http://127.0.0.1:9862')
	self.username = kwargs.get('username', None)
	self.password = kwargs.get('password', None)
	self.verbose = kwargs.get('verbose', False)
	self.lambda_cache = {}

	self.command_table = {
	    'create-comment': {
		'function': self.apply_sub1,
		'method': 'POST',
		'url_template': 'api/comment/item/{1}.json',
		},
	    'create-item': {
		'function': self.apply,
		'method': 'POST',
		'url_template': 'api/item.json',
		},
	    'create-feed': {
		'function': self.apply,
		'method': 'POST',
		'url_template': 'api/feed.json',
		},
	    'create-tag': {
		'function': self.apply,
		'method': 'POST',
		'url_template': 'api/tag.json',
		},
	    'create-vurl': {
		'function': self.apply,
		'method': 'POST',
		'url_template': 'api/vurl.json',
		},
	    'delete-comment': {
		'function': self.apply_sub1,
		'method': 'DELETE',
		'url_template': 'api/comment/{1}.json',
		'__FAKE_ITERATION_KLUDGE__': 1,
		},
	    'delete-comment-key': {
		'function': self.apply_sub1,
		'method': 'DELETE',
		'url_template': 'api/comment/{1}/{2}.json',
		'__FAKE_ITERATION_KLUDGE__': 2,
		},
	    'delete-item': {
		'function': self.apply_sub1,
		'method': 'DELETE',
		'url_template': 'api/item/{1}.json',
		'__FAKE_ITERATION_KLUDGE__': 1,
		},
	    'delete-item-key': {
		'function': self.apply_sub2,
		'method': 'DELETE',
		'url_template': 'api/item/{1}/{2}.json',
		'__FAKE_ITERATION_KLUDGE__': 2,
		},
	    'delete-registry-key': {
		'function': self.apply_sub1,
		'method': 'DELETE',
		'url_template': 'api/registry/{1}.json',
		'__FAKE_ITERATION_KLUDGE__': 1,
		},
	    'delete-feed': {
		'function': self.apply_sub1,
		'method': 'DELETE',
		'url_template': 'api/feed/{1}.json',
		'__FAKE_ITERATION_KLUDGE__': 1,
		},
	    'delete-feed-key': {
		'function': self.apply_sub2,
		'method': 'DELETE',
		'url_template': 'api/feed/{1}/{2}.json',
		'__FAKE_ITERATION_KLUDGE__': 2,
		},
	    'delete-tag': {
		'function': self.apply_sub1,
		'method': 'DELETE',
		'url_template': 'api/tag/{1}.json',
		'__FAKE_ITERATION_KLUDGE__': 1,
		},
	    'delete-tag-key': {
		'function': self.apply_sub2,
		'method': 'DELETE',
		'url_template': 'api/tag/{1}/{2}.json',
		'__FAKE_ITERATION_KLUDGE__': 2,
		},
	    'delete-vurl': {
		'function': self.apply_sub1,
		'method': 'DELETE',
		'url_template': 'api/vurl/{1}.json',
		'__FAKE_ITERATION_KLUDGE__': 1,
		},
	    'delete-vurl-key': {
		'function': self.apply_sub2,
		'method': 'DELETE',
		'url_template': 'api/vurl/{1}/{2}.json',
		'__FAKE_ITERATION_KLUDGE__': 2,
		},
	    'list-comments': {
		'function': self.apply,
		'method': 'GET',
		'url_template': 'api/comment.json',
		},
	    'list-items': {
		'function': self.apply,
		'method': 'GET',
		'url_template': 'api/item.json',
		},
	    'list-registry': {
		'function': self.apply,
		'method': 'GET',
		'url_template': 'api/registry.json',
		},
	    'list-feeds': {
		'function': self.apply,
		'method': 'GET',
		'url_template': 'api/feed.json',
		},
	    'list-tags': {
		'function': self.apply,
		'method': 'GET',
		'url_template': 'api/tag.json',
		},
	    'list-vurls': {
		'function': self.apply,
		'method': 'GET',
		'url_template': 'api/vurl.json',
		},
	    'read-comment': {
		'function': self.apply_sub1,
		'method': 'GET',
		'url_template': 'api/comment/{1}.json',
		},
	    'read-comment-key': {
		'function': self.apply_sub2,
		'method': 'GET',
		'url_template': 'api/comment/{1}/{2}.json',
		},

	    'read-data': {
		'function': None,
		'method': 'GET',
		'url_template': 'api/data/IID',
		},
	    'read-icon': {
		'function': None,
		'method': 'GET',
		'url_template': 'api/icon/IID',
		},

	    'read-item': {
		'function': self.apply_sub1,
		'method': 'GET',
		'url_template': 'api/item/{1}.json',
		},
	    'read-item-key': {
		'function': self.apply_sub2,
		'method': 'GET',
		'url_template': 'api/item/{1}/{2}.json',
		},
	    'read-registry-key': {
		'function': self.apply_sub1,
		'method': 'GET',
		'url_template': 'api/registry/{1}.json',
		},
	    'read-feed': {
		'function': self.apply_sub1,
		'method': 'GET',
		'url_template': 'api/feed/{1}.json',
		},
	    'read-feed-key': {
		'function': self.apply_sub2,
		'method': 'GET',
		'url_template': 'api/feed/{1}/{2}.json',
		},
	    'read-tag': {
		'function': self.apply_sub1,
		'method': 'GET',
		'url_template': 'api/tag/{1}.json',
		},
	    'read-tag-key': {
		'function': self.apply_sub2,
		'method': 'GET',
		'url_template': 'api/tag/{1}/{2}.json',
		},
	    'read-vurl': {
		'function': self.apply_sub1,
		'method': 'GET',
		'url_template': 'api/vurl/{1}.json',
		},
	    'read-vurl-key': {
		'function': self.apply_sub2,
		'method': 'GET',
		'url_template': 'api/vurl/{1}/{2}.json',
		},
	    'update-comment': {
		'function': self.apply_sub1,
		'method': 'POST',
		'url_template': 'api/comment/{1}.json',
		},
	    'update-item': {
		'function': self.apply_sub1,
		'method': 'POST',
		'url_template': 'api/item/{1}.json',
		},
	    'update-registry-key': {
		'function': self.apply_sub1_regkey,
		'method': 'POST',
		'url_template': 'api/registry/{1}.json',
		},
	    'update-feed': {
		'function': self.apply_sub1,
		'method': 'POST',
		'url_template': 'api/feed/{1}.json',
		},
	    'update-tag': {
		'function': self.apply_sub1,
		'method': 'POST',
		'url_template': 'api/tag/{1}.json',
		},
	    'update-vurl': {
		'function': self.apply_sub1,
		'method': 'POST',
		'url_template': 'api/vurl/{1}.json',
		},
	    'version': {
		'function': self.apply,
		'method': 'GET',
		'url_template': 'api/version.json',
		},

	    'login': {
		'function': self.apply,
		'method': 'POST',
		'url_template': 'login.html',
		'skip_login_check': True,
		},
	    'logout': {
		'function': self.apply,
		'method': 'GET',
		'url_template': 'logout.html',
		},
	    }

	if self.username and self.password:
	    self.login()

    ##################################################################

    # STUFF WHICH COMPLEMENTS INITIALISATION / LOGIN / LOGOUT

    def set_url_prefix(self, url_prefix):
	"""
	Define the 'http://site.domain:port' to access your mine, if
	not already provided to __init__()
	"""
	self.url_prefix = url_prefix

    def login(self, **kwargs):
	"""
	Establish session cookies.  Accepts 'username' and 'password'
	kwargs, overriding any provided in __init__()
	"""
	username = kwargs.get('username', self.username)
	if not username:
	    raise RuntimeError, 'no username provided'

	password = kwargs.get('password', self.password)
	if not password:
	    raise RuntimeError, 'no password provided'
	self.call('login', username=username, password=password)

    def logout(self, **kwargs):
	"""
	Call the mine to destroy any session cookies
	"""
	self.call('logout')

    ##################################################################

    # STUFF WHICH TALKS TO THE MINE VIA THE REST API

    def url_call(self, method, url_suffix, form_data):
	"""
	"""
	url = "%s/%s" % (self.url_prefix, url_suffix)
	encoded_data = None

	if self.output_format:
	    url = re.sub(r'\.json$', r'.%s' % self.output_format, url)

	if self.verbose:
	    print "**** send"
	    print "> %s %s %s" % (method, url, str(form_data))

	if method == 'DELETE':
	    form_data['_method'] = 'DELETE'
	    encoded_data = urllib.urlencode(form_data)
	    request = urllib2.Request(url, encoded_data)
	    response = urllib2.urlopen(request)
	elif method == 'POST':
	    if '_method' in form_data:
		raise RuntimeError, 'inexplicable use of _method in POST: %s' % form_data['_method']

	    print "1>", url
	    print "2>", form_data

	    if True: # hardcode the old method for the moment
		encoded_data = urllib.urlencode(form_data)
		print "3>", encoded_data
		request = urllib2.Request(url, encoded_data)
		print "4>", request
                response = urllib2.urlopen(request)
                print "5>", response
	    else:
		datagen, headers = multipart_encode(form_data)
		print "3>", datagen, headers
		request = urllib2.Request(url, datagen, headers)
		print "4>", request
                response = poster_opener.open(request)
                print "5>", response

	elif method == 'GET':
	    request = urllib2.Request(url)
	    response = urllib2.urlopen(request)
	else:
	    raise RuntimeError, 'unknown method: %s' % method

	retval = response.read()

	if self.verbose:
	    print "**** receive"
	    print response.geturl()
	    print response.info()
	    print "****"

	return retval

    ##################################################################

    # STUFF WHICH WRAPS AROUND THE REST-API INVOCATIONS

    def apply(self, method, url_template, *args, **kwargs):
	"""
	Invokes url with method using kwargs as POST data if
	appropriate.  Completely ignores args.
	"""
	url_suffix = url_template
	return self.url_call(method, url_suffix, kwargs)

    def apply_sub1(self, method, url_template, *args, **kwargs):
	"""
	Replaces '{1}' in url_template with arg[0]; invokes resulting
	url with method using kwargs as POST data if appropriate.
	"""
	url_suffix = url_template.replace('{1}', str(args[0]))
	return self.url_call(method, url_suffix, kwargs)

    def apply_sub1_regkey(self, method, url_template, *args, **kwargs):
	"""
	Replaces 'E{lb}1E{rb}' in url_template with arg[0]; invokes resulting
	url with method using faked-up kwargs:

	E{lb} arg[0] : arg[1] E{rb} # eg: E{lb} 'foo': 42 E{rb}

	...because this syntax is used to populate individual keys in
	the registry (applying E{lb} 'foo':42 E{rb} to /api/registry/foo.json)
	"""

	url_suffix = url_template.replace('{1}', args[0])
	kwargs = { args[0] : args[1] }
	return self.url_call(method, url_suffix, kwargs)

    def apply_sub2(self, method, url_template, *args, **kwargs):
	"""
	Replaces '{1}' in url_template with arg[0]; replaces '{2}' in
	url_template with arg[1]; invokes resulting url with method
	using kwargs as POST data if appropriate.
	"""
	url_suffix = url_template.replace('{1}', str(args[0])).replace('{2}', str(args[1]))
	return self.url_call(method, url_suffix, kwargs)

    ##################################################################

    # STUFF WHICH INVOKES THE WRAPPERS

    def call(self, command, *args, **kwargs):
	"""
	invokes the apply() function and parameters associated with
	the command, and returns the (presumably) JSON string that
	results.

	'args' are interpolated into the template (if applicable)

	'kwargs' become POST data (if applicable and not overridden)
	"""

	if command in self.command_table:
	    cmdopts = self.command_table[command]
	    function = cmdopts.get('function', None)
	    method = cmdopts.get('method', None)
	    template = cmdopts.get('url_template', None)
	    retval = function(method, template, *args, **kwargs)
	    if not retval:
		raise RuntimeError, 'request returned no data'
	    return retval
	else:
	    raise RuntimeError, 'unknown command: %s' % command

    def call_py(self, command, *args, **kwargs):
	"""
	Exactly as-per call() but the result is decoded into a
	python data structure and is returned.

	Do NOT set the format to anything other than default(None -
	implying json) if you are using this or any of the virtual
	methods that are provided by __getattr__()
	"""
	return simplejson.loads(self.call(command, *args, **kwargs))

    ##################################################################

    # CREATE VIRTUAL METHODS
    # so api.list_tags() does what you expect

    def __getattr__(self, attr):
	"""
	this getattr overrides the default and via a clever and
	slightly evil kludge implements the following virtual methods:

	create_comment() create_item() create_feed() create_tag()
	create_vurl() delete_comment() delete_comment_key()
	delete_item() delete_item_key() delete_registry_key()
	delete_feed() delete_feed_key() delete_tag()
	delete_tag_key() delete_vurl() delete_vurl_key()
	list_comments() list_items() list_registry() list_feeds()
	list_tags() list_vurls() read_comment() read_comment_key()
	read_data() read_item() read_item_key() read_registry_key()
	read_feed() read_feed_key() read_tag() read_tag_key()
	read_vurl() read_vurl_key() update_comment() update_item()
	update_registry_key() update_feed() update_tag()
	update_vurl() version()

	so you can do stuff like:

	m = MineAPI(username='fred, ...')
	tags = m.list_tags()

	...even though no list_tags() method is defined; this works
	because __getattr__() traps the attempt to access the
	nonexistent list_tags method, converts underscores to hyphens
	and then returns a lambda that frontends call_py() with
	the properly 'command' inserted.

	The net result is: any 'foo-bar' API call is also available as
	api.foo_bar() yielding python structures.
	"""

	command = attr.replace('_', '-')

	if command in self.lambda_cache:
	    return self.lambda_cache[command]

	if command in self.command_table: # is valid
	    self.lambda_cache[command] = lambda *args, **kwargs: self.call_py(command, *args, **kwargs)
	    return self.lambda_cache[command]

	raise AttributeError, 'unknown attribute %s (command %s)' % (attr, command)

    ##################################################################

    # PARSE AND EXECUTE

    def command_line(self, cmdargs):
	"""
	Takes an argument list, and executes it

	Any arguments not containing the '=' character go into a
	dictionary of kwargs that are passed into the followup
	methods, and eventually into POST data

	Example: create-tag tagName="foo" tagDescription="example tag"

	Any arguments not containing the '=' character are appended to
	a plain list that is supplied to the wrapper around the REST
	API invocation, which may (if you are doing it right) iterate
	over those arguments and do something useful.

	Example: delete-tag 1 2 5 7 9 ...

	These concepts probably can mix-and-match, but it'd be deeply
	advanced for anyone to try doing so at the moment.

	This routine also kludges a loop construct atop the api calls
	for most/all of the deletion routines, for the benefit of
	command_line users ONLY; programmers talking to the API are
	expected to use iteration.
	"""

	command = cmdargs.pop(0)
	args = []
	kwargs = {}

	if command in self.command_table:
	    cmdopts = self.command_table[command]
	else:
	    raise RuntimeError, 'unknown command: %s' % command

	iteration_kludge = cmdopts.get('__FAKE_ITERATION_KLUDGE__', 0)

	if iteration_kludge == 0:
	    for x in cmdargs:
		try:
		    i = x.index('=')
		    k = x[0:i]
		    v = x[i+1:]
		    kwargs[k] = v
		except ValueError:
		    args.append(x)
	    print self.call(command, *args, **kwargs)
	elif iteration_kludge == 1:
	    for x in cmdargs:
		args[0] = x
		print self.call(command, *args, **kwargs)
	elif iteration_kludge == 2:
	    args[0] = cmdargs.pop(0)
	    for x in cmdargs:
		args[1] = x
		print self.call(command, *args, **kwargs)

##################################################################
##################################################################
##################################################################
##################################################################
##################################################################

# miner.py [opts ...] command [args ...]
# options:
# -m / --mine http://site.domain:port
# -u / --user username
# -p / --password password
# -v / --verbose
# TODO: GETOPT THIS

if __name__ == "__main__":

    def usage():
	print "usage: miner [options] command [cmdopts]"
	print "options:"
	print "\t-h, --help     # this message"
	print "\t-u X, --user=X # sets mine username, default: pickaxe"
	print "\t-p X, --pass=X # sets mine password, default: (user input)"
	print "\t-m X, --mine=X # sets mine URL, default: http://127.0.0.1:9862"
	print "\t-x, --xml      # sets XML output, default: JSON"
	print "\t-v, --verbose  # verbose mode, default: off"

    shortopts = 'hu:p:m:xv'
    longopts = [ 'help',
		 'user=',
		 'pass=',
		 'username=',
		 'password=',
		 'mine=',
		 'xml',
		 'verbose',
		 ]

    try:
	opts, args = getopt.getopt(sys.argv[1:], shortopts, longopts)
    except getopt.GetoptError, err:
	print str(err)
	usage()
	sys.exit(1)

    # defaults
    mine_root = os.environ.get('MINE_ROOT_URL', 'http://127.0.0.1:9862')
    username = os.environ.get('MINE_USER', 'pickaxe')
    password = None
    verbose = False
    xml = False

    for o, a in opts:
	if o in ('-h', '--help'):
	    usage()
	    sys.exit(0)
	elif o in ('-m', '--mine'):
	    mine_root = a
	elif o in ('-u', '--user', '--username'):
	    username = a
	elif o in ('-p', '--pass', '--password'):
	    password = a
	elif o in ('-v', '--verbose'):
	    verbose = True
	elif o in ('-x', '--xml'):
	    xml = True
	else:
	    assert False, "unhandled option"

    # anything to do?
    if len(args) < 1:
	usage()
	sys.exit(1)

    # last ditch
    if not password:
	password = getpass.getpass()

    apiopts = dict(url_prefix=mine_root,
		   username=username,
		   verbose=verbose,
		   password=password)

    if xml:
	apiopts['output_format'] = 'xml'

    # what are we doing?
    if verbose:
	print '+ %s at %s' % (username, mine_root)

    m = MineAPI(**apiopts)

    try:
	m.command_line(args)

    except HTTPError as e:
	print e
	print e.read()
