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

from django.conf.urls.defaults import *
from django.contrib import admin

import views as mine
from views import REST

admin.autodiscover()

urlpatterns = patterns('',
		       (r'^api/', include('mine.api.urls')),
		       (r'^ui/', include('mine.ui.urls')),
		       (r'^get/', include('mine.get.urls')),
		       (r'^sys/', include('mine.sys.urls')),

                       (r'^pub$', REST, {'GET': mine.read_pub_root}),
                       (r'^doc$', REST, {'GET': mine.read_doc_root}),
                       (r'^$', REST, {'GET': mine.read_mine_root}),
                       )

