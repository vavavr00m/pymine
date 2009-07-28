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

from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404

def RESPOND(request, *args, **kwargs):
    get_view = kwargs.pop('GET', None)
    post_view = kwargs.pop('POST', None)

    if request.method == 'GET' and get_view is not None:
        return get_view(request, *args, **kwargs)
    elif request.method == 'POST' and post_view is not None:
        return post_view(request, *args, **kwargs)

    raise Http404

##################################################################

## url: /ui/create-comment/IID.html
## method: read_create_comment
## args: iid
def read_create_comment(request, iid, *args, **kwargs):
    raise Http404('method read_create_comment for url /ui/create-comment/IID.html is not yet implemented')

## url: /ui/create-item.html
## method: read_create_item
## args: 
def read_create_item(request, *args, **kwargs):
    raise Http404('method read_create_item for url /ui/create-item.html is not yet implemented')

## url: /ui/create-relation.html
## method: read_create_relation
## args: 
def read_create_relation(request, *args, **kwargs):
    raise Http404('method read_create_relation for url /ui/create-relation.html is not yet implemented')

## url: /ui/create-tag.html
## method: read_create_tag
## args: 
def read_create_tag(request, *args, **kwargs):
    raise Http404('method read_create_tag for url /ui/create-tag.html is not yet implemented')

## url: /ui/delete-comment/IID/CID.html
## method: read_delete_comment
## args: iid cid
def read_delete_comment(request, iid, cid, *args, **kwargs):
    raise Http404('method read_delete_comment for url /ui/delete-comment/IID/CID.html is not yet implemented')

## url: /ui/delete-item/IID.html
## method: read_delete_item
## args: iid
def read_delete_item(request, iid, *args, **kwargs):
    raise Http404('method read_delete_item for url /ui/delete-item/IID.html is not yet implemented')

## url: /ui/delete-relation/RID.html
## method: read_delete_relation
## args: rid
def read_delete_relation(request, rid, *args, **kwargs):
    raise Http404('method read_delete_relation for url /ui/delete-relation/RID.html is not yet implemented')

## url: /ui/delete-tag/TID.html
## method: read_delete_tag
## args: tid
def read_delete_tag(request, tid, *args, **kwargs):
    raise Http404('method read_delete_tag for url /ui/delete-tag/TID.html is not yet implemented')

## url: /ui/list-comments/IID.html
## method: read_list_comments
## args: iid
def read_list_comments(request, iid, *args, **kwargs):
    raise Http404('method read_list_comments for url /ui/list-comments/IID.html is not yet implemented')

## url: /ui/list-items.html
## method: read_list_items
## args: 
def read_list_items(request, *args, **kwargs):
    raise Http404('method read_list_items for url /ui/list-items.html is not yet implemented')

## url: /ui/list-relations.html
## method: read_list_relations
## args: 
def read_list_relations(request, *args, **kwargs):
    raise Http404('method read_list_relations for url /ui/list-relations.html is not yet implemented')

## url: /ui/list-tags.html
## method: read_list_tags
## args: 
def read_list_tags(request, *args, **kwargs):
    raise Http404('method read_list_tags for url /ui/list-tags.html is not yet implemented')

## url: /ui/read-comment/IID/CID.html
## method: read_read_comment
## args: iid cid
def read_read_comment(request, iid, cid, *args, **kwargs):
    raise Http404('method read_read_comment for url /ui/read-comment/IID/CID.html is not yet implemented')

## url: /ui/read-config.html
## method: read_read_config
## args: 
def read_read_config(request, *args, **kwargs):
    raise Http404('method read_read_config for url /ui/read-config.html is not yet implemented')

## url: /ui/read-item/IID.html
## method: read_read_item
## args: iid
def read_read_item(request, iid, *args, **kwargs):
    raise Http404('method read_read_item for url /ui/read-item/IID.html is not yet implemented')

## url: /ui/read-relation/RID.html
## method: read_read_relation
## args: rid
def read_read_relation(request, rid, *args, **kwargs):
    raise Http404('method read_read_relation for url /ui/read-relation/RID.html is not yet implemented')

## url: /ui/read-tag/TID.html
## method: read_read_tag
## args: tid
def read_read_tag(request, tid, *args, **kwargs):
    raise Http404('method read_read_tag for url /ui/read-tag/TID.html is not yet implemented')

## url: /ui/update-comment/IID/CID.html
## method: read_update_comment
## args: iid cid
def read_update_comment(request, iid, cid, *args, **kwargs):
    raise Http404('method read_update_comment for url /ui/update-comment/IID/CID.html is not yet implemented')

## url: /ui/update-config.html
## method: read_update_config
## args: 
def read_update_config(request, *args, **kwargs):
    raise Http404('method read_update_config for url /ui/update-config.html is not yet implemented')

## url: /ui/update-item/IID.html
## method: read_update_item
## args: iid
def read_update_item(request, iid, *args, **kwargs):
    raise Http404('method read_update_item for url /ui/update-item/IID.html is not yet implemented')

## url: /ui/update-relation/RID.html
## method: read_update_relation
## args: rid
def read_update_relation(request, rid, *args, **kwargs):
    raise Http404('method read_update_relation for url /ui/update-relation/RID.html is not yet implemented')

## url: /ui/update-tag/TID.html
## method: read_update_tag
## args: tid
def read_update_tag(request, tid, *args, **kwargs):
    raise Http404('method read_update_tag for url /ui/update-tag/TID.html is not yet implemented')

## url: /ui/version.html
## method: read_version.html
## args: 
def read_version(request, *args, **kwargs):
    raise Http404('method read_version.html for url /ui/version.html is not yet implemented')

