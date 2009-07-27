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
from mine import views

admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', views.root),
    (r'^get/', views.rest, {'GET': views.read_get, 'POST': views.create_get}),
    (r'^api/', include('mine.api.urls')),
    (r'^ui/', include('mine.ui.urls')),
)
