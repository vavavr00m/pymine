#!/usr/bin/python
##
## Copyright 2010 Adriana Lukas & Alec Muffett
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
from pymine.views import HTTP_METHOD, mine_redirect
import views as ui

urlpatterns = patterns('',
		       )

##################################################################
# this code is auto-generated.
# ensure that any changes are made via the generator.

urlpatterns += patterns('',
                        (r'^create/comment/(?P<idz>\d+)\.html$',
                         HTTP_METHOD, { 'GET' : [ ui.create_comment, 'create/comment.html' ], }),
                        (r'^create/feed\.html$',
                         HTTP_METHOD, { 'GET' : [ ui.render, 'create/feed.html' ], }),
                        (r'^create/item\.html$',
                         HTTP_METHOD, { 'GET' : [ ui.render, 'create/item.html' ], }),
                        (r'^create/tag\.html$',
                         HTTP_METHOD, { 'GET' : [ ui.render, 'create/tag.html' ], }),
                        (r'^create/vurl\.html$',
                         HTTP_METHOD, { 'GET' : [ ui.render, 'create/vurl.html' ], }),
                        (r'^dash/comments\.html$',
                         HTTP_METHOD, { 'GET' : [ ui.dash_comments, 'dash/comments.html' ], }),
                        (r'^dash/feeds\.html$',
                         HTTP_METHOD, { 'GET' : [ ui.dash_feeds, 'dash/feeds.html' ], }),
                        (r'^dash/home\.html$',
                         HTTP_METHOD, { 'GET' : [ ui.render, 'dash/home.html' ], }),
                        (r'^dash/items\.html$',
                         HTTP_METHOD, { 'GET' : [ ui.dash_items, 'dash/items.html' ], }),
                        (r'^dash/search\.html$',
                         HTTP_METHOD, { 'GET' : [ ui.render, 'dash/search.html' ], }),
                        (r'^dash/settings\.html$',
                         HTTP_METHOD, { 'GET' : [ ui.render, 'dash/settings.html' ], }),
                        (r'^dash/tags\.html$',
                         HTTP_METHOD, { 'GET' : [ ui.dash_tags, 'dash/tags.html' ], }),
                        (r'^dash/vurls\.html$',
                         HTTP_METHOD, { 'GET' : [ ui.dash_vurls, 'dash/vurls.html' ], }),
                        (r'^delete/comment/(?P<id>[1-9]\d*)\.html$',
                         HTTP_METHOD, { 'GET' : [ ui.delete_comment, 'delete/comment.html' ], }),
                        (r'^delete/feed/(?P<id>[1-9]\d*)\.html$',
                         HTTP_METHOD, { 'GET' : [ ui.delete_feed, 'delete/feed.html' ], }),
                        (r'^delete/item/(?P<id>[1-9]\d*)\.html$',
                         HTTP_METHOD, { 'GET' : [ ui.delete_item, 'delete/item.html' ], }),
                        (r'^delete/tag/(?P<id>[1-9]\d*)\.html$',
                         HTTP_METHOD, { 'GET' : [ ui.delete_tag, 'delete/tag.html' ], }),
                        (r'^delete/vurl/(?P<id>[1-9]\d*)\.html$',
                         HTTP_METHOD, { 'GET' : [ ui.delete_vurl, 'delete/vurl.html' ], }),
                        (r'^list/comments/(?P<idz>\d+)\.html$',
                         HTTP_METHOD, { 'GET' : [ ui.list_comments, 'list/comments.html' ], }),
                        (r'^list/feeds\.html$',
                         HTTP_METHOD, { 'GET' : [ ui.list_feeds, 'list/feeds.html' ], }),
                        (r'^list/items\.html$',
                         HTTP_METHOD, { 'GET' : [ ui.list_items, 'list/items.html' ], }),
                        (r'^list/tags\.html$',
                         HTTP_METHOD, { 'GET' : [ ui.list_tags, 'list/tags.html' ], }),
                        (r'^list/vurls\.html$',
                         HTTP_METHOD, { 'GET' : [ ui.list_vurls, 'list/vurls.html' ], }),
                        (r'^read/comment/(?P<id>[1-9]\d*)\.html$',
                         HTTP_METHOD, { 'GET' : [ ui.read_comment, 'read/comment.html' ], }),
                        (r'^read/feed/(?P<id>[1-9]\d*)\.html$',
                         HTTP_METHOD, { 'GET' : [ ui.read_feed, 'read/feed.html' ], }),
                        (r'^read/item/(?P<id>[1-9]\d*)\.html$',
                         HTTP_METHOD, { 'GET' : [ ui.read_item, 'read/item.html' ], }),
                        (r'^read/tag/(?P<id>[1-9]\d*)\.html$',
                         HTTP_METHOD, { 'GET' : [ ui.read_tag, 'read/tag.html' ], }),
                        (r'^read/vurl/(?P<id>[1-9]\d*)\.html$',
                         HTTP_METHOD, { 'GET' : [ ui.read_vurl, 'read/vurl.html' ], }),
                        (r'^search/comments\.html$',
                         HTTP_METHOD, { 'GET' : [ ui.search_comments, 'search/comments.html' ], }),
                        (r'^search/feeds\.html$',
                         HTTP_METHOD, { 'GET' : [ ui.search_feeds, 'search/feeds.html' ], }),
                        (r'^search/items\.html$',
                         HTTP_METHOD, { 'GET' : [ ui.search_items, 'search/items.html' ], }),
                        (r'^search/tags\.html$',
                         HTTP_METHOD, { 'GET' : [ ui.search_tags, 'search/tags.html' ], }),
                        (r'^search/vurls\.html$',
                         HTTP_METHOD, { 'GET' : [ ui.search_vurls, 'search/vurls.html' ], }),
                        (r'^update/comment/(?P<id>[1-9]\d*)\.html$',
                         HTTP_METHOD, { 'GET' : [ ui.update_comment, 'update/comment.html' ], }),
                        (r'^update/feed/(?P<id>[1-9]\d*)\.html$',
                         HTTP_METHOD, { 'GET' : [ ui.update_feed, 'update/feed.html' ], }),
                        (r'^update/item/(?P<id>[1-9]\d*)\.html$',
                         HTTP_METHOD, { 'GET' : [ ui.update_item, 'update/item.html' ], }),
                        (r'^update/tag/(?P<id>[1-9]\d*)\.html$',
                         HTTP_METHOD, { 'GET' : [ ui.update_tag, 'update/tag.html' ], }),
                        (r'^update/vurl/(?P<id>[1-9]\d*)\.html$',
                         HTTP_METHOD, { 'GET' : [ ui.update_vurl, 'update/vurl.html' ], }),
                        (r'^version\.html$',
                         HTTP_METHOD, { 'GET' : [ ui.version, 'version.html' ], }),
                        )

##################################################################
