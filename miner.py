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
Miner: 
provides the MineAPI class for client development, 
*and* the commandline uploader for pymine.
"""

import os
import sys
import getopt
import getpass
import urllib
import urllib2
import cookielib

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

        self.cookie_file = kwargs.get('cookie_file', 'etc/cookies2.txt')
        self.cookie_jar = cookielib.LWPCookieJar(self.cookie_file)

        if (os.path.isfile(self.cookie_file)):
            self.cookie_jar.load()

        urllib2.install_opener(urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie_jar)))

        self.command_list = {
            # 'command': ( handler, method, url_template ),

            'login': ( self.apply_direct, 'POST', 'login.html' ),
            'logout': ( self.apply_direct, 'GET', 'logout.html' ),
            'version': ( self.apply_direct, 'GET', 'api/version.json' ),

            'read-data': ( self.dummy, 'GET', 'api/item/IID' ),

            'delete-registry-key': ( self.apply_sub1_direct, 'DELETE', 'api/registry/{1}.json' ),
            'list-registry': ( self.apply_direct, 'GET', 'api/registry.json' ),
            'read-registry-key': ( self.apply_sub1_direct, 'GET', 'api/registry/{1}.json' ),
            'update-registry-key': ( self.apply_sub1_regkey, 'POST', 'api/registry/{1}.json' ),

            'create-comment': ( self.apply_sub1_direct, 'POST', 'api/comment/item/{1}.json' ),
            'create-item': ( self.apply_direct, 'POST', 'api/item.json' ),
            'create-relation': ( self.apply_direct, 'POST', 'api/relation.json' ),
            'create-tag': ( self.apply_direct, 'POST', 'api/tag.json' ),
            'create-vurl': ( self.apply_direct, 'POST', 'api/vurl.json' ),

            'delete-comment-key': ( self.apply_sub1_subevery, 'DELETE', 'api/comment/{1}/{2}.json' ),
            'delete-item-key': ( self.apply_sub1_subevery, 'DELETE', 'api/item/{1}/{2}.json' ),
            'delete-relation-key': ( self.apply_sub1_subevery, 'DELETE', 'api/relation/{1}/{2}.json' ),
            'delete-tag-key': ( self.apply_sub1_subevery, 'DELETE', 'api/tag/{1}/{2}.json' ),
            'delete-vurl-key': ( self.apply_sub1_subevery, 'DELETE', 'api/vurl/{1}/{2}.json' ),

            'delete-comment': ( self.apply_subevery, 'DELETE', 'api/comment/{1}.json' ),
            'delete-item': ( self.apply_subevery, 'DELETE', 'api/item/{1}.json' ),
            'delete-relation': ( self.apply_subevery, 'DELETE', 'api/relation/{1}.json' ),
            'delete-tag': ( self.apply_subevery, 'DELETE', 'api/tag/{1}.json' ),
            'delete-vurl': ( self.apply_subevery, 'DELETE', 'api/vurl/{1}.json' ),

            'list-comments': ( self.apply_direct, 'GET', 'api/comment.json' ),
            'list-items': ( self.apply_direct, 'GET', 'api/item.json' ),
            'list-relations': ( self.apply_direct, 'GET', 'api/relation.json' ),
            'list-tags': ( self.apply_direct, 'GET', 'api/tag.json' ),
            'list-vurls': ( self.apply_direct, 'GET', 'api/vurl.json' ),

            'read-comment-key': ( self.apply_sub2_direct, 'GET', 'api/comment/{1}/{2}.json' ),
            'read-item-key': ( self.apply_sub2_direct, 'GET', 'api/item/{1}/{2}.json' ),
            'read-relation-key': ( self.apply_sub2_direct, 'GET', 'api/relation/{1}/{2}.json' ),
            'read-tag-key': ( self.apply_sub2_direct, 'GET', 'api/tag/{1}/{2}.json' ),
            'read-vurl-key': ( self.apply_sub2_direct, 'GET', 'api/vurl/{1}/{2}.json' ),

            'read-comment': ( self.apply_sub1_direct, 'GET', 'api/comment/{1}.json' ),
            'read-item': ( self.apply_sub1_direct, 'GET', 'api/item/{1}.json' ),
            'read-relation': ( self.apply_sub1_direct, 'GET', 'api/relation/{1}.json' ),
            'read-tag': ( self.apply_sub1_direct, 'GET', 'api/tag/{1}.json' ),
            'read-vurl': ( self.apply_sub1_direct, 'GET', 'api/vurl/{1}.json' ),

            'update-comment': ( self.apply_sub1_direct, 'POST', 'api/comment/{1}.json' ),
            'update-item': ( self.apply_sub1_direct, 'POST', 'api/item/{1}.json' ),
            'update-relation': ( self.apply_sub1_direct, 'POST', 'api/relation/{1}.json' ),
            'update-tag': ( self.apply_sub1_direct, 'POST', 'api/tag/{1}.json' ),
            'update-vurl': ( self.apply_sub1_direct, 'POST', 'api/vurl/{1}.json' ),

            }

        if self.username and self.password:
            self.login()

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
    ##################################################################
    ##################################################################

    def url_call(self, method, url_suffix, form_data):

        url = "%s/%s" % (self.url_prefix, url_suffix)
        encoded_data = None

        print "> %s %s %s" % (method, url, str(form_data))

        if method == 'DELETE':
            return '' # TBD HACK
        elif method == 'POST':
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

    def dummy(self, method, url_template, *args, **kwargs):
        """
        Do nothing useful 
        """
        return [ ]

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

    def call(self, command, *args, **kwargs):
        """
        Args get interpolated into the template (if applicable) and
        Kwargs become POST data (if applicable and not overridden)
        """

        if command in self.command_list:
            function, method, template = self.command_list[command]
            retval = function(method, template, *args, **kwargs)
            if not retval: raise RuntimeError, 'request returned no data'
            return retval
        else:
            raise RuntimeError, 'unknown command: %s' % command

    ##################################################################
    ##################################################################
    ##################################################################

    def parse(self, command, *arglist):
        """
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

    @classmethod
    def batch(klass, filename):
	pass

##################################################################
##################################################################
##################################################################

if __name__ == "__main__":

    username = 'pickaxe'
    password = getpass.getpass()

    m = MineAPI(username=username, password=password)

    command = sys.argv[1]
    arglist = sys.argv[2:]

    try:
        retlist = m.parse(command, *arglist)

        for x in retlist:
            print x

        m.save_cookies() # probably pointless since session cookies are not marked persistent

    except HTTPError as e:
        print e
        print e.read()



