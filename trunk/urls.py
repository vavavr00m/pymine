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

from django.conf.urls.defaults import *
from django.contrib import admin

import views as mine
from views import REST

admin.autodiscover()

urlpatterns = patterns('',
		       (r'^ui/', include('ui.urls')),
		       (r'^get/', include('get.urls')),
		       (r'^api/', include('api.urls')),

		       (r'^admin/doc/', \
                            include('django.contrib.admindocs.urls')),

		       (r'^admin/(.*)', admin.site.root),

                       (r'^login.html$', \
                            'django.contrib.auth.views.login', \
                            { 'template_name': 'users/login.html' }),

                       (r'^logout.html$', \
                            'django.contrib.auth.views.logout', \
                            { 'template_name': 'users/logout.html' }),

		       #################################

		       (r'^pub/(?P<suffix>.+)$', REST, { 'GET': mine.handle_pub }),
		       (r'^pub/$', REST, { 'GET': mine.root_pub }),
		       (r'^favicon\.ico$', REST, { 'GET': mine.root_favicon }),
		       (r'^$', REST, { 'GET': mine.root_mine }),
)
