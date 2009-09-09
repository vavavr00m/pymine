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

from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404

import pymine.api.views as api

##################################################################

## rest: GET /ui
## function: read_ui_root
## declared args: 
def read_ui_root(request, *args, **kwargs):
    return render_to_response('read-ui-root.html')

## rest: GET /ui/create-comment/IID.html
## function: create_comment
## declared args: iid
def create_comment(request, iid, *args, **kwargs):
    return render_to_response('create-comment.html')

## rest: GET /ui/create-item.html
## function: create_item
## declared args: 
def create_item(request, *args, **kwargs):
    return render_to_response('create-item.html')

## rest: GET /ui/create-relation.html
## function: create_relation
## declared args: 
def create_relation(request, *args, **kwargs):
    return render_to_response('create-relation.html')

## rest: GET /ui/create-tag.html
## function: create_tag
## declared args: 
def create_tag(request, *args, **kwargs):
    return render_to_response('create-tag.html')

## rest: GET /ui/delete-comment/CID.html
## function: delete_comment
## declared args: cid
def delete_comment(request, cid, *args, **kwargs):
    return render_to_response('delete-comment.html')

## rest: GET /ui/delete-item/IID.html
## function: delete_item
## declared args: iid
def delete_item(request, iid, *args, **kwargs):
    return render_to_response('delete-item.html')

## rest: GET /ui/delete-relation/RID.html
## function: delete_relation
## declared args: rid
def delete_relation(request, rid, *args, **kwargs):
    return render_to_response('delete-relation.html')

## rest: GET /ui/delete-tag/TID.html
## function: delete_tag
## declared args: tid
def delete_tag(request, tid, *args, **kwargs):
    return render_to_response('delete-tag.html')

## rest: GET /ui/list-comments/IID.html
## function: list_comments
## declared args: iid
def list_comments(request, iid, *args, **kwargs):
    s = api.list_comments(None, iid)
    return render_to_response('list-comments.html', s)

## rest: GET /ui/list-items.html
## function: list_items
## declared args: 
def list_items(request, *args, **kwargs):
    s = api.list_items(None)
    return render_to_response('list-items.html', s)

## rest: GET /ui/list-relations.html
## function: list_relations
## declared args: 
def list_relations(request, *args, **kwargs):
    s = api.list_relations(None)
    return render_to_response('list-relations.html', s)

## rest: GET /ui/list-tags.html
## function: list_tags
## declared args: 
def list_tags(request, *args, **kwargs):
    s = api.list_tags(None)
    return render_to_response('list-tags.html', s)

## rest: GET /ui/read-comment/CID.html
## function: read_comment
## declared args: cid
def read_comment(request, cid, *args, **kwargs):
    return render_to_response('read-comment.html')

## rest: GET /ui/read-item/IID.html
## function: read_item
## declared args: iid
def read_item(request, iid, *args, **kwargs):
    return render_to_response('read-item.html')

## rest: GET /ui/read-registry.html
## function: read_registry
## declared args: 
def read_registry(request, *args, **kwargs):
    return render_to_response('read-registry.html')

## rest: GET /ui/read-relation/RID.html
## function: read_relation
## declared args: rid
def read_relation(request, rid, *args, **kwargs):
    return render_to_response('read-relation.html')

## rest: GET /ui/read-tag/TID.html
## function: read_tag
## declared args: tid
def read_tag(request, tid, *args, **kwargs):
    return render_to_response('read-tag.html')

## rest: GET /ui/update-comment/CID.html
## function: update_comment
## declared args: cid
def update_comment(request, cid, *args, **kwargs):
    return render_to_response('update-comment.html')

## rest: GET /ui/update-item/IID.html
## function: update_item
## declared args: iid
def update_item(request, iid, *args, **kwargs):
    return render_to_response('update-item.html')

## rest: GET /ui/update-registry.html
## function: update_registry
## declared args: 
def update_registry(request, *args, **kwargs):
    return render_to_response('update-registry.html')

## rest: GET /ui/update-relation/RID.html
## function: update_relation
## declared args: rid
def update_relation(request, rid, *args, **kwargs):
    return render_to_response('update-relation.html')

## rest: GET /ui/update-tag/TID.html
## function: update_tag
## declared args: tid
def update_tag(request, tid, *args, **kwargs):
    return render_to_response('update-tag.html')

## rest: GET /ui/version.html
## function: version
## declared args: 
def version(request, *args, **kwargs):
    s = api.read_version(None)
    return render_to_response('version.html', s)

