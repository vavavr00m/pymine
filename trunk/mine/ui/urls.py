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

urlpatterns = patterns('',
    (r'^create-comment/(?P<iid>\d+).html$',
     ui.RESPOND, {'GET': ui.read_create_comment}),
    (r'^create-item.html$',
     ui.RESPOND, {'GET': ui.read_create_item}),
    (r'^create-relation.html$',
     ui.RESPOND, {'GET': ui.read_create_relation}),
    (r'^create-tag.html$',
     ui.RESPOND, {'GET': ui.read_create_tag}),
    (r'^delete-comment/(?P<iid>\d+)/(?P<cid>\d+).html$',
     ui.RESPOND, {'GET': ui.read_delete_comment}),
    (r'^delete-item/(?P<iid>\d+).html$',
     ui.RESPOND, {'GET': ui.read_delete_item}),
    (r'^delete-relation/(?P<rid>\d+).html$',
     ui.RESPOND, {'GET': ui.read_delete_relation}),
    (r'^delete-tag/(?P<tid>\d+).html$',
     ui.RESPOND, {'GET': ui.read_delete_tag}),
    (r'^list-comments/(?P<iid>\d+).html$',
     ui.RESPOND, {'GET': ui.read_list_comments}),
    (r'^list-items.html$',
     ui.RESPOND, {'GET': ui.read_list_items}),
    (r'^list-relations.html$',
     ui.RESPOND, {'GET': ui.read_list_relations}),
    (r'^list-tags.html$',
     ui.RESPOND, {'GET': ui.read_list_tags}),
    (r'^read-comment/(?P<iid>\d+)/(?P<cid>\d+).html$',
     ui.RESPOND, {'GET': ui.read_read_comment}),
    (r'^read-config.html$',
     ui.RESPOND, {'GET': ui.read_read_config}),
    (r'^read-item/(?P<iid>\d+).html$',
     ui.RESPOND, {'GET': ui.read_read_item}),
    (r'^read-relation/(?P<rid>\d+).html$',
     ui.RESPOND, {'GET': ui.read_read_relation}),
    (r'^read-tag/(?P<tid>\d+).html$',
     ui.RESPOND, {'GET': ui.read_read_tag}),
    (r'^update-comment/(?P<iid>\d+)/(?P<cid>\d+).html$',
     ui.RESPOND, {'GET': ui.read_update_comment}),
    (r'^update-config.html$',
     ui.RESPOND, {'GET': ui.read_update_config}),
    (r'^update-item/(?P<iid>\d+).html$',
     ui.RESPOND, {'GET': ui.read_update_item}),
    (r'^update-relation/(?P<rid>\d+).html$',
     ui.RESPOND, {'GET': ui.read_update_relation}),
    (r'^update-tag/(?P<tid>\d+).html$',
     ui.RESPOND, {'GET': ui.read_update_tag}),
    (r'^version.html$',
     ui.RESPOND, {'GET': ui.read_version}),
)
