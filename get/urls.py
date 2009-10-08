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

import views as get
from pymine.views import REST

urlpatterns = patterns('',
                       (r'^v/(?P<suffix>.+)$',
                        REST, { 'GET': get.redirect_vurlname }),
                       (r'^r/(?P<vurlkey>[A-Za-z0-9!@]+)$',
                        REST, { 'GET': get.redirect_vurlkey }),
                       (r'^i/(?P<vid>[1-9]\d*)$',
                        REST, { 'GET': get.redirect_vid }),
                       (r'^(?P<minekey>[A-Za-z0-9!@]+)$',
                        REST, { 'GET': get.read_minekey,
                                'POST': get.submit_minekey }),
                       (r'^$',
                        REST, { 'GET': get.root_get }),
                       )
