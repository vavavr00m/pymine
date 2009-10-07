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

import views as ui
from pymine.views import REST

urlpatterns = patterns('',
                       (r'^version\.html$',
                        REST, { 'GET': ui.read_version }),
                       (r'^update-vurl/(?P<vid>[1-9]\d*)\.html$',
                        REST, { 'GET': ui.update_vurl }),
                       (r'^update-tag/(?P<tid>[1-9]\d*)\.html$',
                        REST, { 'GET': ui.update_tag }),
                       (r'^update-relation/(?P<rid>[1-9]\d*)\.html$',
                        REST, { 'GET': ui.update_relation }),
                       (r'^update-item/(?P<iid>\d+)\.html$',
                        REST, { 'GET': ui.update_item }),
                       (r'^update-comment/(?P<cid>[1-9]\d*)\.html$',
                        REST, { 'GET': ui.update_comment }),
                       (r'^read-vurl/(?P<vid>[1-9]\d*)\.html$',
                        REST, { 'GET': ui.read_vurl }),
                       (r'^read-tag/(?P<tid>[1-9]\d*)\.html$',
                        REST, { 'GET': ui.read_tag }),
                       (r'^read-relation/(?P<rid>[1-9]\d*)\.html$',
                        REST, { 'GET': ui.read_relation }),
                       (r'^read-item/(?P<iid>\d+)\.html$',
                        REST, { 'GET': ui.read_item }),
                       (r'^read-comment/(?P<cid>[1-9]\d*)\.html$',
                        REST, { 'GET': ui.read_comment }),
                       (r'^list-vurls\.html$',
                        REST, { 'GET': ui.list_vurls }),
                       (r'^list-tags\.html$',
                        REST, { 'GET': ui.list_tags }),
                       (r'^list-relations\.html$',
                        REST, { 'GET': ui.list_relations }),
                       (r'^list-items\.html$',
                        REST, { 'GET': ui.list_items }),
                       (r'^list-comments/(?P<iid>\d+)\.html$',
                        REST, { 'GET': ui.list_comments }),
                       (r'^delete-vurl/(?P<vid>[1-9]\d*)\.html$',
                        REST, { 'GET': ui.delete_vurl }),
                       (r'^delete-tag/(?P<tid>[1-9]\d*)\.html$',
                        REST, { 'GET': ui.delete_tag }),
                       (r'^delete-relation/(?P<rid>[1-9]\d*)\.html$',
                        REST, { 'GET': ui.delete_relation }),
                       (r'^delete-item/(?P<iid>\d+)\.html$',
                        REST, { 'GET': ui.delete_item }),
                       (r'^delete-comment/(?P<cid>[1-9]\d*)\.html$',
                        REST, { 'GET': ui.delete_comment }),
                       (r'^create-vurl\.html$',
                        REST, { 'GET': ui.create_vurl }),
                       (r'^create-tag\.html$',
                        REST, { 'GET': ui.create_tag }),
                       (r'^create-relation\.html$',
                        REST, { 'GET': ui.create_relation }),
                       (r'^create-item\.html$',
                        REST, { 'GET': ui.create_item }),
                       (r'^create-comment/(?P<iid>\d+)\.html$',
                        REST, { 'GET': ui.create_comment }),
                       (r'^$',
                        REST, { 'GET': ui.root_ui }),
		       )
