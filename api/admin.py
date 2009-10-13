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

from models import Tag, Relation, Item, Comment, Vurl
from models import TagXattr, RelationXattr, ItemXattr, CommentXattr, VurlXattr
from models import Registry, LogEvent

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

class LogEventAdmin(admin.ModelAdmin):
    list_display = ('status', 'ip', 'type', 'method', 'path', 'key', 'msg', 'last_modified', 'created')
    search_fields = ['type', 'msg']
    list_filter = ['created']
    date_hierarchy = 'created'

admin.site.register(LogEvent, LogEventAdmin)

##################################################################

class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'last_modified', 'created')
    search_fields = ['name', 'description']
    list_filter = ['created']
    date_hierarchy = 'created'
    fieldsets = [
        (None, {'fields': ['name']}), 
        ('Advanced', {'fields': ['description', 'implies']}), 
        ]

admin.site.register(Tag, TagAdmin)

##################################################################

class RelationAdmin(admin.ModelAdmin):
    list_display = ('name', 'version', 'last_modified', 'created')
    search_fields = ['name', 'description']
    list_filter = ['created']
    date_hierarchy = 'created'
    fieldsets = [
        (None, {'fields': ['name', 'version', 'description']}), 
        ('Tags', {'fields': ['tags', 'tags_required', 'tags_excluded']}), 
        ('Advanced', {'fields': ['network_pattern', 'embargo_before', 'embargo_after'], 'classes': ['collapse']}), 
        ]

admin.site.register(Relation, RelationAdmin)

##################################################################

class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'content_type', 'last_modified', 'created')
    search_fields = ['name', 'description']
    list_filter = ['created']
    date_hierarchy = 'created'
    fieldsets = [
        (None, {'fields': ['name', 'status', 'data', 'content_type', 'description']}), 
        ('Tags', {'fields': ['tags', 'item_for_relations', 'item_not_relations']}), 
        ('Advanced', {'fields': ['feed_link', 'hide_before', 'hide_after'], 'classes': ['collapse']}), 
        ]

admin.site.register(Item, ItemAdmin)

##################################################################

class CommentAdmin(admin.ModelAdmin):
    list_display = ('title', 'relation',  'item', 'last_modified', 'created')
    search_fields = ['title', 'body']
    list_filter = ['created']
    date_hierarchy = 'created'
    fieldsets = [
        (None, {'fields': ['title', 'body']}), 
        ('Advanced', {'fields': ['item', 'relation']}), 
        ]

admin.site.register(Comment, CommentAdmin)

##################################################################

class VurlAdmin(admin.ModelAdmin):
    list_display = ('name', 'link', 'last_modified', 'created')
    search_fields = ['name']
    list_filter = ['created']
    date_hierarchy = 'created'
    fieldsets = [
        (None, {'fields': ['name', 'link']}), 
        ]

admin.site.register(Vurl, VurlAdmin)

##################################################################

class TagXattrAdmin(admin.ModelAdmin):
    list_display = ('tag', 'key', 'value', 'last_modified', 'created')
    search_fields = ['key', 'value']
    list_filter = ['created']
    date_hierarchy = 'created'

admin.site.register(TagXattr, TagXattrAdmin)

##################################################################

class CommentXattrAdmin(admin.ModelAdmin):
    list_display = ('comment', 'key', 'value', 'last_modified', 'created')
    search_fields = ['key', 'value']
    list_filter = ['created']
    date_hierarchy = 'created'

admin.site.register(CommentXattr, CommentXattrAdmin)

##################################################################

class ItemXattrAdmin(admin.ModelAdmin):
    list_display = ('item', 'key', 'value', 'last_modified', 'created')
    search_fields = ['key', 'value']
    list_filter = ['created']
    date_hierarchy = 'created'

admin.site.register(ItemXattr, ItemXattrAdmin)

##################################################################

class RelationXattrAdmin(admin.ModelAdmin):
    list_display = ('relation', 'key', 'value', 'last_modified', 'created')
    search_fields = ['key', 'value']
    list_filter = ['created']
    date_hierarchy = 'created'

admin.site.register(RelationXattr, RelationXattrAdmin)

##################################################################

class VurlXattrAdmin(admin.ModelAdmin):
    list_display = ('vurl', 'key', 'value', 'last_modified', 'created')
    search_fields = ['key', 'value']
    list_filter = ['created']
    date_hierarchy = 'created'

admin.site.register(VurlXattr, VurlXattrAdmin)

##################################################################
##################################################################
##################################################################
