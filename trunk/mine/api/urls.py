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
from mine.views import API_CALL, REST

urlpatterns = patterns('',
    (r'^vurl/(?P<tid>\d+)/(?P<key>\w+).(?P<fmt>(xml|json|py))$', API_CALL,
     {'DELETE': api.delete_vurl_key, 'GET': api.get_vurl_key}),
    (r'^vurl/(?P<tid>\d+).(?P<fmt>(xml|json|py))$', API_CALL,
     {'DELETE': api.delete_vurl, 'GET': api.read_vurl, 'POST': api.update_vurl}),
    (r'^vurl.(?P<fmt>(xml|json|py))$', API_CALL,
     {'GET': api.list_vurls, 'POST': api.create_vurl}),
    (r'^version.(?P<fmt>(xml|json|py))$', API_CALL,
     {'GET': api.read_version}),
    (r'^url/(?P<rid>\d+)/(?P<rvsn>\d+)/(?P<iid>\d+).(?P<fmt>(xml|json|py))$', API_CALL,
     {'GET': api.encode_minekey3}),
    (r'^url/(?P<rid>\d+)/(?P<iid>\d+).(?P<fmt>(xml|json|py))$', API_CALL,
     {'GET': api.encode_minekey2}),
    (r'^url/(?P<rid>\d+).(?P<fmt>(xml|json|py))$', API_CALL,
     {'GET': api.encode_minekey1}),
    (r'^tag/(?P<tid>\d+)/(?P<key>\w+).(?P<fmt>(xml|json|py))$', API_CALL,
     {'DELETE': api.delete_tag_key, 'GET': api.get_tag_key}),
    (r'^tag/(?P<tid>\d+).(?P<fmt>(xml|json|py))$', API_CALL,
     {'DELETE': api.delete_tag, 'GET': api.read_tag, 'POST': api.update_tag}),
    (r'^tag.(?P<fmt>(xml|json|py))$', API_CALL,
     {'GET': api.list_tags, 'POST': api.create_tag}),
    (r'^select/vurl.(?P<fmt>(xml|json|py))$', API_CALL,
     {'GET': api.read_select_tag}),
    (r'^select/tag.(?P<fmt>(xml|json|py))$', API_CALL,
     {'GET': api.read_select_tag}),
    (r'^select/relation.(?P<fmt>(xml|json|py))$', API_CALL,
     {'GET': api.read_select_relation}),
    (r'^select/item.(?P<fmt>(xml|json|py))$', API_CALL,
     {'GET': api.read_select_item}),
    (r'^relation/(?P<rid>\d+)/(?P<key>\w+).(?P<fmt>(xml|json|py))$', API_CALL,
     {'DELETE': api.delete_relation_key, 'GET': api.get_relation_key}),
    (r'^relation/(?P<rid>\d+).(?P<fmt>(xml|json|py))$', API_CALL,
     {'DELETE': api.delete_relation, 'GET': api.read_relation, 'POST': api.update_relation}),
    (r'^relation.(?P<fmt>(xml|json|py))$', API_CALL,
     {'GET': api.list_relations, 'POST': api.create_relation}),
    (r'^registry/(?P<key>\w+).(?P<fmt>(xml|json|py))$', API_CALL,
     {'POST': api.amend_registry_key, 'DELETE': api.delete_registry_key, 'GET': api.get_registry_key}),
    (r'^registry.(?P<fmt>(xml|json|py))$', API_CALL,
     {'GET': api.list_registry}),
    (r'^item/(?P<iid>\d+)/(?P<key>\w+).(?P<fmt>(xml|json|py))$', API_CALL,
     {'DELETE': api.delete_item_key, 'GET': api.get_item_key}),
    (r'^item/(?P<iid>\d+).(?P<fmt>(xml|json|py))$', API_CALL,
     {'DELETE': api.delete_item, 'GET': api.read_item, 'POST': api.update_item}),
    (r'^item/(?P<iid>\d+)$', REST,
     {'GET': api.read_item_data}),
    (r'^item.(?P<fmt>(xml|json|py))$', API_CALL,
     {'GET': api.list_items, 'POST': api.create_item}),
    (r'^comment/item/(?P<iid>\d+).(?P<fmt>(xml|json|py))$', API_CALL,
     {'GET': api.list_comments, 'POST': api.create_comment}),
    (r'^comment/(?P<cid>\d+)/(?P<key>\w+).(?P<fmt>(xml|json|py))$', API_CALL,
     {'DELETE': api.delete_comment_key, 'GET': api.get_comment_key}),
    (r'^comment/(?P<cid>\d+).(?P<fmt>(xml|json|py))$', API_CALL,
     {'DELETE': api.delete_comment, 'GET': api.read_comment, 'POST': api.update_comment}),
    (r'^clone/(?P<iid>\d+).(?P<fmt>(xml|json|py))$', API_CALL,
     {'GET': api.list_clones, 'POST': api.create_clone}),
    (r'^$', REST,
     {'GET': api.read_api_root}),
		       )
