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
from pymine.api.models import Tag, Item, Feed, Comment, Vurl
from pymine.views import HTTP_AUTH, mine_redirect
import pymine.ui.views as ui

urlpatterns = patterns('',
		       )

##################################################################
# this code is auto-generated.
# ensure that any changes are made via the generator.

urlpatterns += patterns('',
			(r'^create/comment/(?P<idz>\d+)\.html$',
			 HTTP_AUTH, { 'GET' : [ ui.create_comment, 'create/comment.html' ], }),
			(r'^create/feed\.html$',
			 HTTP_AUTH, { 'GET' : [ ui.render_page, 'create/feed.html' ], }),
			(r'^create/item\.html$',
			 HTTP_AUTH, { 'GET' : [ ui.render_page, 'create/item.html' ], }),
			(r'^create/tag\.html$',
			 HTTP_AUTH, { 'GET' : [ ui.render_page, 'create/tag.html' ], }),
			(r'^create/vurl\.html$',
			 HTTP_AUTH, { 'GET' : [ ui.render_page, 'create/vurl.html' ], }),
			(r'^dash/comments\.html$',
			 HTTP_AUTH, { 'GET' : [ ui.dash_comments, 'dash/comments.html' ], }),
			(r'^dash/feeds\.html$',
			 HTTP_AUTH, { 'GET' : [ ui.dash_things, 'dash/feeds.html', Feed ], }),
			(r'^dash/home\.html$',
			 HTTP_AUTH, { 'GET' : [ ui.render_page, 'dash/home.html' ], }),
			(r'^dash/items\.html$',
			 HTTP_AUTH, { 'GET' : [ ui.dash_things, 'dash/items.html', Item ], }),
			(r'^dash/search\.html$',
			 HTTP_AUTH, { 'GET' : [ ui.render_page, 'dash/search.html' ], }),
			(r'^dash/settings\.html$',
			 HTTP_AUTH, { 'GET' : [ ui.render_page, 'dash/settings.html' ], }),
			(r'^dash/tags\.html$',
			 HTTP_AUTH, { 'GET' : [ ui.dash_things, 'dash/tags.html', Tag ], }),
			(r'^dash/vurls\.html$',
			 HTTP_AUTH, { 'GET' : [ ui.dash_things, 'dash/vurls.html', Vurl ], }),
			(r'^delete/comment/(?P<id>[1-9]\d*)\.html$',
			 HTTP_AUTH, { 'GET' : [ ui.delete_thing, 'delete/comment.html', 'commentId' ], }),
			(r'^delete/feed/(?P<id>[1-9]\d*)\.html$',
			 HTTP_AUTH, { 'GET' : [ ui.delete_thing, 'delete/feed.html', 'feedId' ], }),
			(r'^delete/item/(?P<id>[1-9]\d*)\.html$',
			 HTTP_AUTH, { 'GET' : [ ui.delete_thing, 'delete/item.html', 'itemId' ], }),
			(r'^delete/tag/(?P<id>[1-9]\d*)\.html$',
			 HTTP_AUTH, { 'GET' : [ ui.delete_thing, 'delete/tag.html', 'tagId' ], }),
			(r'^delete/vurl/(?P<id>[1-9]\d*)\.html$',
			 HTTP_AUTH, { 'GET' : [ ui.delete_thing, 'delete/vurl.html', 'vurlId' ], }),
			(r'^list/comments/(?P<idz>\d+)\.html$',
			 HTTP_AUTH, { 'GET' : [ ui.list_comments, 'list/comments.html' ], }),
			(r'^list/feeds\.html$',
			 HTTP_AUTH, { 'GET' : [ ui.list_things, 'list/feeds.html', Feed ], }),
			(r'^list/items\.html$',
			 HTTP_AUTH, { 'GET' : [ ui.list_things, 'list/items.html', Item ], }),
			(r'^list/tags\.html$',
			 HTTP_AUTH, { 'GET' : [ ui.list_things, 'list/tags.html', Tag ], }),
			(r'^list/vurls\.html$',
			 HTTP_AUTH, { 'GET' : [ ui.list_things, 'list/vurls.html', Vurl ], }),
			(r'^read/comment/(?P<id>[1-9]\d*)\.html$',
			 HTTP_AUTH, { 'GET' : [ ui.read_thing, 'read/comment.html', Comment ], }),
			(r'^read/feed/(?P<id>[1-9]\d*)\.html$',
			 HTTP_AUTH, { 'GET' : [ ui.read_thing, 'read/feed.html', Feed ], }),
			(r'^read/item/(?P<id>[1-9]\d*)\.html$',
			 HTTP_AUTH, { 'GET' : [ ui.read_thing, 'read/item.html', Item ], }),
			(r'^read/tag/(?P<id>[1-9]\d*)\.html$',
			 HTTP_AUTH, { 'GET' : [ ui.read_thing, 'read/tag.html', Tag ], }),
			(r'^read/vurl/(?P<id>[1-9]\d*)\.html$',
			 HTTP_AUTH, { 'GET' : [ ui.read_thing, 'read/vurl.html', Vurl ], }),
			(r'^search/comments\.html$',
			 HTTP_AUTH, { 'GET' : [ ui.render_page, 'search/comments.html' ], }),
			(r'^search/feeds\.html$',
			 HTTP_AUTH, { 'GET' : [ ui.render_page, 'search/feeds.html' ], }),
			(r'^search/items\.html$',
			 HTTP_AUTH, { 'GET' : [ ui.render_page, 'search/items.html' ], }),
			(r'^search/tags\.html$',
			 HTTP_AUTH, { 'GET' : [ ui.render_page, 'search/tags.html' ], }),
			(r'^search/vurls\.html$',
			 HTTP_AUTH, { 'GET' : [ ui.render_page, 'search/vurls.html' ], }),
			(r'^update/comment/(?P<id>[1-9]\d*)\.html$',
			 HTTP_AUTH, { 'GET' : [ ui.update_thing, 'update/comment.html', Comment ], }),
			(r'^update/feed/(?P<id>[1-9]\d*)\.html$',
			 HTTP_AUTH, { 'GET' : [ ui.update_thing, 'update/feed.html', Feed ], }),
			(r'^update/item/(?P<id>[1-9]\d*)\.html$',
			 HTTP_AUTH, { 'GET' : [ ui.update_thing, 'update/item.html', Item ], }),
			(r'^update/tag/(?P<id>[1-9]\d*)\.html$',
			 HTTP_AUTH, { 'GET' : [ ui.update_thing, 'update/tag.html', Tag ], }),
			(r'^update/vurl/(?P<id>[1-9]\d*)\.html$',
			 HTTP_AUTH, { 'GET' : [ ui.update_thing, 'update/vurl.html', Vurl ], }),
			(r'^version\.html$',
			 HTTP_AUTH, { 'GET' : [ ui.version, 'read/version.html' ], }),
			)

##################################################################
