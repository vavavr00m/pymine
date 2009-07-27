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
from frontend import views
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', views.root),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/(.*)', admin.site.root),
    (r'^api/config.(?P<fmt>(xml|json|html|txt))$', views.rest, {'GET': views.read_config, 'POST': views.create_config}),
    (r'^api/item.(?P<fmt>(xml|json|html|txt))$', views.rest, {'GET': views.read_item_list, 'POST': views.create_item}),
    (r'^api/item/(?P<iid>\d+)$', views.rest, {'GET': views.read_item_data, 'PUT': views.update_item_data}),
    (r'^api/item/(?P<iid>\d+).(?P<fmt>(xml|json|html|txt))$', views.rest, {'DELETE': views.delete_item, 'GET': views.read_item}),
    (r'^api/item/(?P<iid>\d+)/(?P<cid>\d+).(?P<fmt>(xml|json|html|txt))$', views.rest, {'DELETE': views.delete_comment, 'GET': views.read_comment}),
    (r'^api/item/(?P<iid>\d+)/(?P<cid>\d+)/key.(?P<fmt>(xml|json|html|txt))$', views.rest, {'POST': views.create_comment_key}),
    (r'^api/item/(?P<iid>\d+)/(?P<cid>\d+)/key/(?P<key>\w+).(?P<fmt>(xml|json|html|txt))$', views.rest, {'DELETE': views.delete_comment_key, 'GET': views.read_comment_key, 'PUT': views.update_comment_key}),
    (r'^api/item/(?P<iid>\d+)/clone.(?P<fmt>(xml|json|html|txt))$', views.rest, {'GET': views.read_clone_list, 'POST': views.create_clone}),
    (r'^api/item/(?P<iid>\d+)/comment.(?P<fmt>(xml|json|html|txt))$', views.rest, {'GET': views.read_comment_list, 'POST': views.create_comment}),
    (r'^api/item/(?P<iid>\d+)/key.(?P<fmt>(xml|json|html|txt))$', views.rest, {'POST': views.create_item_key}),
    (r'^api/item/(?P<iid>\d+)/key/(?P<key>\w+).(?P<fmt>(xml|json|html|txt))$', views.rest, {'DELETE': views.delete_item_key, 'GET': views.read_item_key, 'PUT': views.update_item_key}),
    (r'^api/relation.(?P<fmt>(xml|json|html|txt))$', views.rest, {'GET': views.read_relation_list, 'POST': views.create_relation}),
    (r'^api/relation/(?P<rid>\d+).(?P<fmt>(xml|json|html|txt))$', views.rest, {'DELETE': views.delete_relation, 'GET': views.read_relation}),
    (r'^api/relation/(?P<rid>\d+)/key.(?P<fmt>(xml|json|html|txt))$', views.rest, {'POST': views.create_relation_key}),
    (r'^api/relation/(?P<rid>\d+)/key/(?P<key>\w+).(?P<fmt>(xml|json|html|txt))$', views.rest, {'DELETE': views.delete_relation_key, 'GET': views.read_relation_key, 'PUT': views.update_relation_key}),
    (r'^api/tag.(?P<fmt>(xml|json|html|txt))$', views.rest, {'GET': views.read_tag_list, 'POST': views.create_tag}),
    (r'^api/tag/(?P<tid>\d+).(?P<fmt>(xml|json|html|txt))$', views.rest, {'DELETE': views.delete_tag, 'GET': views.read_tag}),
    (r'^api/tag/(?P<tid>\d+)/key.(?P<fmt>(xml|json|html|txt))$', views.rest, {'POST': views.create_tag_key}),
    (r'^api/tag/(?P<tid>\d+)/key/(?P<key>\w+).(?P<fmt>(xml|json|html|txt))$', views.rest, {'DELETE': views.delete_tag_key, 'GET': views.read_tag_key, 'PUT': views.update_tag_key}),
    (r'^api/version.(?P<fmt>(xml|json|html|txt))$', views.rest, {'GET': views.read_version}),
)
