#!/usr/bin/python
##
## Copyright 2009-2010 Adriana Lukas & Alec Muffett
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

from pymine.api.models import Tag, Feed, Item, Comment, Vurl
from pymine.api.models import TagXattr, FeedXattr, ItemXattr, CommentXattr, VurlXattr
from pymine.api.models import Registry

from django.contrib import admin

##################################################################

class RegistryAdmin(admin.ModelAdmin):
    list_display = ('key', 'value', 'last_modified', 'created')
    search_fields = ['key']
    list_filter = ['created']
    date_hierarchy = 'created'
    fieldsets = [
	(None, {'fields': ['key', 'value']}),
	]

admin.site.register(Registry, RegistryAdmin)

##################################################################
##################################################################
##################################################################
##################################################################
##################################################################

class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'last_modified', 'created')
    search_fields = ['name', 'description']
    list_filter = ['created']
    date_hierarchy = 'created'
    fieldsets = [
	(None, {'fields': ['name', 'is_deleted']}),
	('Advanced', {'fields': ['description', 'implies']}),
	]

admin.site.register(Tag, TagAdmin)

##################################################################

class FeedAdmin(admin.ModelAdmin):
    list_display = ('name', 'version', 'last_modified', 'created')
    search_fields = ['name', 'description']
    list_filter = ['created']
    date_hierarchy = 'created'
    fieldsets = [
	(None, {'fields': ['name', 'is_deleted', 'version', 'description']}),
	('Interests', {'fields': ['interests', 'interests_require', 'interests_exclude']}),
	('Advanced', {'fields': ['permitted_networks',
				 'content_constraints',
				 'embargo_before',
				 'embargo_after',
				 'is_considered_public',
				 ]}),
	]

admin.site.register(Feed, FeedAdmin)

##################################################################

class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'data_type', 'last_modified', 'created', 'hide_before', 'hide_after')
    search_fields = ['name', 'description']
    list_filter = ['created']
    date_hierarchy = 'created'
    fieldsets = [
	(None, {'fields': ['name', 'is_deleted', 'status', 
                           'is_considered_public', 'description']}),
	('Data', {'fields': ['data_type',
			     'data',
			     'icon_type',
			     'icon',
			     'links_to_items',
			     ]}),
	('Tags', {'fields': ['tags', 'for_feeds', 'not_feeds']}),
	('Advanced', {'fields': ['hide_before', 'hide_after']}),
	]

admin.site.register(Item, ItemAdmin)

##################################################################

class CommentAdmin(admin.ModelAdmin):
    list_display = ('title', 'from_feed',  'upon_item', 'last_modified', 'created')
    search_fields = ['title', 'body']
    list_filter = ['created']
    date_hierarchy = 'created'
    fieldsets = [
	(None, {'fields': ['title', 'is_deleted', 'body']}),
	('Advanced', {'fields': ['upon_item', 'from_feed']}),
	]

admin.site.register(Comment, CommentAdmin)

##################################################################

class VurlAdmin(admin.ModelAdmin):
    list_display = ('name', 'link', 
                    'use_temporary_redirect', 'last_modified', 'created')
    search_fields = ['name']
    list_filter = ['created']
    date_hierarchy = 'created'
    fieldsets = [
	(None, {'fields': ['name', 'is_deleted', 'link', 'use_temporary_redirect']}),
	('Advanced', {'fields': ['invalid_before', 'invalid_after']}),
	]

admin.site.register(Vurl, VurlAdmin)

##################################################################
##################################################################
##################################################################
##################################################################
##################################################################

class TagXattrAdmin(admin.ModelAdmin):
    list_display = ('parent', 'key', 'value', 'last_modified', 'created')
    search_fields = ['key', 'value']
    list_filter = ['created']
    date_hierarchy = 'created'

admin.site.register(TagXattr, TagXattrAdmin)

##################################################################

class CommentXattrAdmin(admin.ModelAdmin):
    list_display = ('parent', 'key', 'value', 'last_modified', 'created')
    search_fields = ['key', 'value']
    list_filter = ['created']
    date_hierarchy = 'created'

admin.site.register(CommentXattr, CommentXattrAdmin)

##################################################################

class ItemXattrAdmin(admin.ModelAdmin):
    list_display = ('parent', 'key', 'value', 'last_modified', 'created')
    search_fields = ['key', 'value']
    list_filter = ['created']
    date_hierarchy = 'created'

admin.site.register(ItemXattr, ItemXattrAdmin)

##################################################################

class FeedXattrAdmin(admin.ModelAdmin):
    list_display = ('parent', 'key', 'value', 'last_modified', 'created')
    search_fields = ['key', 'value']
    list_filter = ['created']
    date_hierarchy = 'created'

admin.site.register(FeedXattr, FeedXattrAdmin)

##################################################################

class VurlXattrAdmin(admin.ModelAdmin):
    list_display = ('parent', 'key', 'value', 'last_modified', 'created')
    search_fields = ['key', 'value']
    list_filter = ['created']
    date_hierarchy = 'created'

admin.site.register(VurlXattr, VurlXattrAdmin)

##################################################################
##################################################################
##################################################################
