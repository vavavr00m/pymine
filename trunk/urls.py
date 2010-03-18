#!/usr/bin/env python
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

from django.conf.urls.defaults import *
from django.contrib import admin

import pymine.views as mine
from pymine.views import HTTP_AUTH, HTTP_NOAUTH

admin.autodiscover()

urlpatterns = patterns('',
		       (r'^admin/(.*)', admin.site.root),
		       (r'^admin/doc/', include('django.contrib.admindocs.urls')),
		       (r'^login.html$', 'django.contrib.auth.views.login', { 'template_name': 'users/login.html' }),
		       (r'^logout.html$', 'django.contrib.auth.views.logout', { 'template_name': 'users/logout.html' }),
		       (r'^api/', include('api.urls')),
		       (r'^ui/', include('ui.urls')),
		       )

##################################################################
# this code is auto-generated.
# ensure that any changes are made via the generator.

urlpatterns += patterns('',
			(r'^$',
			 HTTP_AUTH, { 'GET' : [ mine.mine_redirect, 'ui/dash/home.html' ], }),
			(r'^favicon\.ico$',
			 HTTP_NOAUTH, { 'GET' : [ mine.get_favicon ], }),
			(r'^key/(?P<mk_hmac>[-\w]{43})/(?P<mk_fid>[1-9]\d*)/(?P<mk_fversion>[1-9]\d*)/(?P<mk_iid>\d+)/(?P<mk_depth>[1-9]\d*)/(?P<mk_type>(data|icon|submit))\.(?P<mk_ext>\w+)$',
			 HTTP_NOAUTH, { 'GET' : [ mine.minekey_read ],
					       'POST' : [ mine.minekey_submit ], }),
			(r'^page/(?P<suffix>.*)$',
			 HTTP_NOAUTH, { 'GET' : [ mine.vurl_read_by_name ], }),
			(r'^pub(/(?P<suffix>.*))?$',
			 HTTP_NOAUTH, { 'GET' : [ mine.mine_public ], }),
			(r'^vurl/(?P<vurlkey>[-\w]+)$',
			 HTTP_NOAUTH, { 'GET' : [ mine.vurl_read_by_key ], }),
			)

##################################################################
