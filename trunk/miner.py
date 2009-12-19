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


# WORK IN PROGRESS - 18 DECEMBER 2009 
# - STILL HAVE TO SORT OUT HOW / WHETHER TO HACK MULTI-VALUE RESULTS.
# - STILL HAVE TO SORT MULTIPART UPLOAD


"""
Miner:
provides the MineAPI class for client development,
*and* the commandline uploader for pymine.
"""

import cookielib
import getopt
import getpass
import os
import sys
import urllib
import urllib2

import django.utils.simplejson as simplejson

from urllib2 import HTTPError

# essential reading:
# http://stackoverflow.com/questions/407468/python-urllib2-file-upload-problems

class MineAPI:
    def __init__(self, **kwargs):
	"""
	Initialise a MineAPI object; Recognised kwargs include:

	output_format
	url_prefix
	username
	password
	cookie_file

	Automatically calls login() if both username and password are given.
	"""

	self.api_format = kwargs.get('output_format', None)

	self.url_prefix = kwargs.get('url_prefix', 'http://127.0.0.1:9862')
	self.username = kwargs.get('username', None)
	self.password = kwargs.get('password', None)
	self.verbose = kwargs.get('verbose', False)


	self.cookie_file = kwargs.get('cookie_file', 'etc/cookies2.txt')
	self.cookie_jar = cookielib.LWPCookieJar(self.cookie_file)

	self.lambda_cache = {}

	if (os.path.isfile(self.cookie_file)):
	    self.cookie_jar.load()

	urllib2.install_opener(urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie_jar)))

	self.command_list = {
	    # 'command': ( handler, method, url_template, multibool ),

	    'login': ( self.apply_direct, 'POST', 'login.html', False ),
	    'logout': ( self.apply_direct, 'GET', 'logout.html', False ),
	    'version': ( self.apply_direct, 'GET', 'api/version.json', False ),

	    'read-data': ( self.dummy, 'GET', 'api/item/IID', False ),

	    'delete-registry-key': ( self.apply_sub1_direct, 'DELETE', 'api/registry/{1}.json', False ),
	    'list-registry': ( self.apply_direct, 'GET', 'api/registry.json', False ),
	    'read-registry-key': ( self.apply_sub1_direct, 'GET', 'api/registry/{1}.json', False ),
	    'update-registry-key': ( self.apply_sub1_regkey, 'POST', 'api/registry/{1}.json', False ),

	    'create-comment': ( self.apply_sub1_direct, 'POST', 'api/comment/item/{1}.json', False ),
	    'create-item': ( self.apply_direct, 'POST', 'api/item.json', False ),
	    'create-relation': ( self.apply_direct, 'POST', 'api/relation.json', False ),
	    'create-tag': ( self.apply_direct, 'POST', 'api/tag.json', False ),
	    'create-vurl': ( self.apply_direct, 'POST', 'api/vurl.json', False ),

	    'delete-comment-key': ( self.apply_sub1_subevery, 'DELETE', 'api/comment/{1}/{2}.json', False ),
	    'delete-item-key': ( self.apply_sub1_subevery, 'DELETE', 'api/item/{1}/{2}.json', False ),
	    'delete-relation-key': ( self.apply_sub1_subevery, 'DELETE', 'api/relation/{1}/{2}.json', False ),
	    'delete-tag-key': ( self.apply_sub1_subevery, 'DELETE', 'api/tag/{1}/{2}.json', False ),
	    'delete-vurl-key': ( self.apply_sub1_subevery, 'DELETE', 'api/vurl/{1}/{2}.json', False ),

	    'delete-comment': ( self.apply_subevery, 'DELETE', 'api/comment/{1}.json', False ),
	    'delete-item': ( self.apply_subevery, 'DELETE', 'api/item/{1}.json', False ),
	    'delete-relation': ( self.apply_subevery, 'DELETE', 'api/relation/{1}.json', False ),
	    'delete-tag': ( self.apply_subevery, 'DELETE', 'api/tag/{1}.json', False ),
	    'delete-vurl': ( self.apply_subevery, 'DELETE', 'api/vurl/{1}.json', False ),

	    'list-comments': ( self.apply_direct, 'GET', 'api/comment.json', False ),
	    'list-items': ( self.apply_direct, 'GET', 'api/item.json', False ),
	    'list-relations': ( self.apply_direct, 'GET', 'api/relation.json', False ),
	    'list-tags': ( self.apply_direct, 'GET', 'api/tag.json', False ),
	    'list-vurls': ( self.apply_direct, 'GET', 'api/vurl.json', False ),

	    'read-comment-key': ( self.apply_sub2_direct, 'GET', 'api/comment/{1}/{2}.json', False ),
	    'read-item-key': ( self.apply_sub2_direct, 'GET', 'api/item/{1}/{2}.json', False ),
	    'read-relation-key': ( self.apply_sub2_direct, 'GET', 'api/relation/{1}/{2}.json', False ),
	    'read-tag-key': ( self.apply_sub2_direct, 'GET', 'api/tag/{1}/{2}.json', False ),
	    'read-vurl-key': ( self.apply_sub2_direct, 'GET', 'api/vurl/{1}/{2}.json', False ),

	    'read-comment': ( self.apply_sub1_direct, 'GET', 'api/comment/{1}.json', False ),
	    'read-item': ( self.apply_sub1_direct, 'GET', 'api/item/{1}.json', False ),
	    'read-relation': ( self.apply_sub1_direct, 'GET', 'api/relation/{1}.json', False ),
	    'read-tag': ( self.apply_sub1_direct, 'GET', 'api/tag/{1}.json', False ),
	    'read-vurl': ( self.apply_sub1_direct, 'GET', 'api/vurl/{1}.json', False ),

	    'update-comment': ( self.apply_sub1_direct, 'POST', 'api/comment/{1}.json', False ),
	    'update-item': ( self.apply_sub1_direct, 'POST', 'api/item/{1}.json', False ),
	    'update-relation': ( self.apply_sub1_direct, 'POST', 'api/relation/{1}.json', False ),
	    'update-tag': ( self.apply_sub1_direct, 'POST', 'api/tag/{1}.json', False ),
	    'update-vurl': ( self.apply_sub1_direct, 'POST', 'api/vurl/{1}.json', False ),

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

    def save_cookies(self):
	"""
	saves any persistent session cookies to disk
	"""
	self.cookie_jar.save()

    ##################################################################

    # STUFF WHICH TALKS TO THE MINE VIA THE REST API

    def url_call(self, method, url_suffix, form_data):
        """        
        """

	url = "%s/%s" % (self.url_prefix, url_suffix)
	encoded_data = None

        if self.verbose:
            print "> %s %s %s" % (method, url, str(form_data))

	if method == 'DELETE':
            form_data['_method'] = 'DELETE'
	    encoded_data = urllib.urlencode(form_data)
	    request = urllib2.Request(url, encoded_data)
	    response = urllib2.urlopen(request)
	elif method == 'POST':
            if '_method' in form_data:
                raise RuntimeError, 'inexplicable use of _method in POST: %s' % form_data['_method']
	    encoded_data = urllib.urlencode(form_data)
	    request = urllib2.Request(url, encoded_data)
	    response = urllib2.urlopen(request)
	elif method == 'GET':
	    request = urllib2.Request(url)
	    response = urllib2.urlopen(request)
	else:
	    raise RuntimeError, 'unknown method: %s' % method

	return response.read()

    ##################################################################

    # STUFF WHICH WRAPS AROUND THE REST-API INVOCATIONS
    # ALWAYS RETURNS A LIST

    def dummy(self, method, url_template, *args, **kwargs):
	"""
	Do nothing useful
	"""
	return []

    def apply_direct(self, method, url_template, *args, **kwargs):
	"""
	Invokes url with method using kwargs as POST data if
	appropriate.  Completely ignores args.
	"""
	url_suffix = url_template
	retval = self.url_call(method, url_suffix, kwargs)
	return [ retval ]

    def apply_sub1_direct(self, method, url_template, *args, **kwargs):
	"""
	Replaces '{1}' in url_template with arg[0]; invokes resulting
	url with method using kwargs as POST data if appropriate.
	"""
	url_suffix = url_template.replace('{1}', args[0])
	retval = self.url_call(method, url_suffix, kwargs)
	return [ retval ]

    def apply_subevery(self, method, url_template, *args, **kwargs):
	"""
	For each arg in args replaces '{1}' in url_template with arg;
	invokes resulting url with method using kwargs as POST data if
	appropriate.
	"""
	retval = []
	for arg in args:
	    url_suffix = url_template.replace('{1}', arg)
	    result = self.url_call(method, url_suffix, kwargs)
	    retval.append(result)
	return retval

    def apply_sub2_direct(self, method, url_template, *args, **kwargs):
	"""
	Replaces '{1}' in url_template with arg[0]; replaces '{2}' in
	url_template with arg[1]; invokes resulting url with method
	using kwargs as POST data if appropriate.
	"""
	url_suffix = url_template.replace('{1}', args[0]).replace('{2}', args[1])
	retval = self.url_call(method, url_suffix, kwargs)
	return [ retval ]

    def apply_sub1_regkey(self, method, url_template, *args, **kwargs):
	"""
	Replaces '{1}' in url_template with arg[0]; invokes resulting
	url with method using faked-up kwargs {arg[0] : arg[1]}; used
	to populate individual keys in the registry.
	"""
	url_suffix = url_template.replace('{1}', args[0])
	kwargs = { args[0] : args[1] }
	retval = self.url_call(method, url_suffix, kwargs)
	return [ retval ]

    def apply_sub1_subevery(self, method, url_template, *args, **kwargs):
	"""
	Replaces '{1}' in url_template with arg[0]; creates new
	template.  For each REMAINING arg in args replaces '{2}' in
	url_template with arg; invokes resulting url with method using
	kwargs as POST data if appropriate.
	"""
	url_template = url_template.replace('{1}', args[0])
	retval = []
	for arg in args[1:]:
	    url_suffix = url_template.replace('{2}', arg)
	    result = self.url_call(method, url_suffix, kwargs)
	    retval.append(result)
	return retval

    ##################################################################

    # STUFF WHICH INVOKES THE WRAPPERS

    def call(self, command, *args, **kwargs):
	"""
	Args get interpolated into the template (if applicable) and
	Kwargs become POST data (if applicable and not overridden)
	"""

	if command in self.command_list:
	    function, method, template, multibool = self.command_list[command]
	    retval = function(method, template, *args, **kwargs)
	    if not retval: raise RuntimeError, 'request returned no data'
	    return retval
	else:
	    raise RuntimeError, 'unknown command: %s' % command

    def call_decode(self, command, *args, **kwargs):
	"""
	"""
	result = self.call(command, *args, **kwargs)
	return [ simplejson.loads(i) for i in result ]

    ##################################################################

    # CREATE VIRTUAL METHODS
    # so api.list_tags() does what you expect

    def __getattr__(self, attr):
	"""
        this getattr overrides the default and via a clever and
        slightly evil kludge implements the following virtual methods:

        create_comment() create_item() create_relation() create_tag()
        create_vurl() delete_comment() delete_comment_key()
        delete_item() delete_item_key() delete_registry_key()
        delete_relation() delete_relation_key() delete_tag()
        delete_tag_key() delete_vurl() delete_vurl_key()
        list_comments() list_items() list_registry() list_relations()
        list_tags() list_vurls() read_comment() read_comment_key()
        read_data() read_item() read_item_key() read_registry_key()
        read_relation() read_relation_key() read_tag() read_tag_key()
        read_vurl() read_vurl_key() update_comment() update_item()
        update_registry_key() update_relation() update_tag()
        update_vurl() version()

        so you can do stuff like:

            m = MineAPI(username='fred, ...')
            tags = m.list_tags()

        ...even though no list_tags() method is defined; this works
        because __getattr__() traps the attempt to access the
        nonexistent list_tags method, converts underscores to hyphens
        and then returns a lambda that frontends call_decode() with
        the properly 'command' inserted.

        The net result is: any 'foo-bar' API call is also available as
        api.foo_bar() yielding python structures.
	"""

	command = attr.replace('_', '-')

	if command in self.lambda_cache:
	    return self.lambda_cache[command]

	if command in self.command_list:
	    function, method, template, multibool = self.command_list[command]
	    self.lambda_cache[command] = lambda *args, **kwargs: self.call_decode(command, *args, **kwargs)
	    return self.lambda_cache[command]

	raise AttributeError, 'unknown attribute %s (command %s)' % (attr, command)

    ##################################################################

    # PARSE AND EXECUTE
    # launch: command arg arg key=val key=val

    def command_execute(self, command, *arglist):
	"""
        takes a command and an argument list, and executes it

        any arguments not containing the '=' character go into a
        dictionary of kwargs that are passed into the followup
        methods, and eventually into POST data

        example: create-tag tagName="foo" tagDescription="example tag"

        any arguments not containing the '=' character are appended to
        a plain list that is supplied to the wrapper around the REST
        API invocation, which may (if you are doing it right) iterate
        over those arguments and do something useful.

        example: delete-tag 1 2 5 7 9 ...

        these concepts probably can mix-and-match, but it'd be deeply
        advanced for anyone to try doing so at the moment.
	"""

	args = []
	kwargs = {}

	for arg in arglist:
	    try:
		i = arg.index('=')
		k = arg[0:i]
		v = arg[i+1:]
		kwargs[k] = v
	    except ValueError:
		args.append(arg)

	retval = self.call(command, *args, **kwargs)
	return retval


##################################################################
##################################################################
##################################################################

# miner.py [opts ...] command [args ...]
# options:
# -u / --user username
# -p / --password password
# -v / --verbose
# -m / --mine http://site.domain:port
# TODO: GETOPT THIS


if __name__ == "__main__":

    u = 'pickaxe'
    p = getpass.getpass()
    v = False
    root = os.environ['MINE_ROOT_URL']
    command = sys.argv[1]
    arglist = sys.argv[2:]

    m = MineAPI(url_prefix=root, username=u, verbose=v, password=p)

    try:
	retlist = m.command_execute(command, *arglist)

	for x in retlist:
	    print x

	m.save_cookies() # probably pointless since session cookies are not marked persistent

    except HTTPError as e:
	print e
	print e.read()
