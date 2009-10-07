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

import views as api
from pymine.views import API_CALL, REST

urlpatterns = patterns('',
                       (r'^vurl\.(?P<fmt>(rdr|xml|json))$',
                        API_CALL, { 'POST': api.create_vurl,
                                    'GET': api.list_vurls }),
                       (r'^vurl/(?P<tid>[1-9]\d*)\.(?P<fmt>(rdr|xml|json))$',
                        API_CALL, { 'DELETE': api.delete_vurl,
                                    'GET': api.read_vurl,
                                    'POST': api.update_vurl }),
                       (r'^vurl/(?P<tid>[1-9]\d*)/(?P<sattr>(__)?[A-Za-z][_A-Za-z]*)\.(?P<safmt>(rdr|xml|json|raw))$',
                        API_CALL, { 'DELETE': api.delete_vurl_key,
                                    'GET': api.get_vurl_key }),
                       (r'^version\.(?P<fmt>(rdr|xml|json))$',
                        API_CALL, { 'GET': api.read_version }),
                       (r'^url/(?P<rid>[1-9]\d*)\.(?P<fmt>(rdr|xml|json))$',
                        API_CALL, { 'GET': api.encode_minekey1 }),
                       (r'^url/(?P<rid>[1-9]\d*)/(?P<rvsn>[1-9]\d*)/(?P<iid>\d+)\.(?P<fmt>(rdr|xml|json))$',
                        API_CALL, { 'GET': api.encode_minekey3 }),
                       (r'^url/(?P<rid>[1-9]\d*)/(?P<iid>\d+)\.(?P<fmt>(rdr|xml|json))$',
                        API_CALL, { 'GET': api.encode_minekey2 }),
                       (r'^tag\.(?P<fmt>(rdr|xml|json))$',
                        API_CALL, { 'POST': api.create_tag,
                                    'GET': api.list_tags }),
                       (r'^tag/(?P<tid>[1-9]\d*)\.(?P<fmt>(rdr|xml|json))$',
                        API_CALL, { 'DELETE': api.delete_tag,
                                    'GET': api.read_tag,
                                    'POST': api.update_tag }),
                       (r'^tag/(?P<tid>[1-9]\d*)/(?P<sattr>(__)?[A-Za-z][_A-Za-z]*)\.(?P<safmt>(rdr|xml|json|raw))$',
                        API_CALL, { 'DELETE': api.delete_tag_key,
                                    'GET': api.get_tag_key }),
                       (r'^select/vurl\.(?P<fmt>(rdr|xml|json))$',
                        API_CALL, { 'GET': api.read_select_tag }),
                       (r'^select/tag\.(?P<fmt>(rdr|xml|json))$',
                        API_CALL, { 'GET': api.read_select_tag }),
                       (r'^select/relation\.(?P<fmt>(rdr|xml|json))$',
                        API_CALL, { 'GET': api.read_select_relation }),
                       (r'^select/item\.(?P<fmt>(rdr|xml|json))$',
                        API_CALL, { 'GET': api.read_select_item }),
                       (r'^relation\.(?P<fmt>(rdr|xml|json))$',
                        API_CALL, { 'POST': api.create_relation,
                                    'GET': api.list_relations }),
                       (r'^relation/(?P<rid>[1-9]\d*)\.(?P<fmt>(rdr|xml|json))$',
                        API_CALL, { 'DELETE': api.delete_relation,
                                    'GET': api.read_relation,
                                    'POST': api.update_relation }),
                       (r'^relation/(?P<rid>[1-9]\d*)/(?P<sattr>(__)?[A-Za-z][_A-Za-z]*)\.(?P<safmt>(rdr|xml|json|raw))$',
                        API_CALL, { 'DELETE': api.delete_relation_key,
                                    'GET': api.get_relation_key }),
                       (r'^registry\.(?P<fmt>(rdr|xml|json))$',
                        API_CALL, { 'GET': api.list_registry }),
                       (r'^registry/(?P<rattr>[A-Za-z][_A-Za-z]*)\.(?P<fmt>(rdr|xml|json))$',
                        API_CALL, { 'POST': api.amend_registry_key,
                                    'DELETE': api.delete_registry_key,
                                    'GET': api.get_registry_key }),
                       (r'^item\.(?P<fmt>(rdr|xml|json))$',
                        API_CALL, { 'POST': api.create_item,
                                    'GET': api.list_items }),
                       (r'^item/(?P<iid>\d+)\.(?P<fmt>(rdr|xml|json))$',
                        API_CALL, { 'DELETE': api.delete_item,
                                    'GET': api.read_item,
                                    'POST': api.update_item }),
                       (r'^item/(?P<iid>\d+)/(?P<sattr>(__)?[A-Za-z][_A-Za-z]*)\.(?P<safmt>(rdr|xml|json|raw))$',
                        API_CALL, { 'DELETE': api.delete_item_key,
                                    'GET': api.get_item_key }),
                       (r'^item/(?P<iid>\d+)$',
                        REST, { 'GET': api.read_item_data }),
                       (r'^ie/import\.(?P<efmt>(zip|tar))$',
                        API_CALL, { 'GET': api.import_mine }),
                       (r'^ie/export\.(?P<efmt>(zip|tar))$',
                        API_CALL, { 'GET': api.export_mine }),
                       (r'^comment/item/(?P<iid>\d+)\.(?P<fmt>(rdr|xml|json))$',
                        API_CALL, { 'POST': api.create_comment,
                                    'GET': api.list_comments }),
                       (r'^comment/(?P<cid>[1-9]\d*)\.(?P<fmt>(rdr|xml|json))$',
                        API_CALL, { 'DELETE': api.delete_comment,
                                    'GET': api.read_comment,
                                    'POST': api.update_comment }),
                       (r'^comment/(?P<cid>[1-9]\d*)/(?P<sattr>(__)?[A-Za-z][_A-Za-z]*)\.(?P<safmt>(rdr|xml|json|raw))$',
                        API_CALL, { 'DELETE': api.delete_comment_key,
                                    'GET': api.get_comment_key }),
                       (r'^clone/(?P<iid>\d+)\.(?P<fmt>(rdr|xml|json))$',
                        API_CALL, { 'POST': api.create_clone,
                                    'GET': api.list_clones }),
                       (r'^$',
                        REST, { 'GET': api.root_api }),
		       )
