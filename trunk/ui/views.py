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

"""docstring goes here""" # :-)

from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404

from pymine.api.models import Tag, Item, Relation, Comment, Vurl
import pymine.api.views as api

##################################################################

## rest: GET /ui/create/comment/IID.html
## function: create_comment
## declared args: iid
def create_comment(request, iid, *args, **kwargs):
    """create_comment(iid) returns ..."""
    s = {'itemId': iid}
    return render_to_response('create/comment.html', s)

## rest: GET /ui/create/item.html
## function: create_item
## declared args: 
def create_item(request, *args, **kwargs):
    """create_item() returns ..."""
    s = {}
    return render_to_response('create/item.html', s)

## rest: GET /ui/create/relation.html
## function: create_relation
## declared args: 
def create_relation(request, *args, **kwargs):
    """create_relation() returns ..."""
    s = {}
    return render_to_response('create/relation.html', s)

## rest: GET /ui/create/tag.html
## function: create_tag
## declared args: 
def create_tag(request, *args, **kwargs):
    """create_tag() returns ..."""
    s = {}
    return render_to_response('create/tag.html', s)

## rest: GET /ui/create/text.html
## function: create_text
## declared args: 
def create_text(request, *args, **kwargs):
    """create_text() returns ..."""
    s = {}
    return render_to_response('create/text.html', s)

## rest: GET /ui/create/vurl.html
## function: create_vurl
## declared args: 
def create_vurl(request, *args, **kwargs):
    """create_vurl() returns ..."""
    s = {}
    return render_to_response('create/vurl.html', s)

## rest: GET /ui/dash/comments.html
## function: dash_comments
## declared args: 
def dash_comments(request, *args, **kwargs):
    """dash_comments() returns ..."""
    s = {}
    return render_to_response('dash/comments.html', s)

## rest: GET /ui/dash/items.html
## function: dash_items
## declared args: 
def dash_items(request, *args, **kwargs):
    """dash_items() returns ..."""
    s = {}
    return render_to_response('dash/items.html', s)

## rest: GET /ui/dash/relations.html
## function: dash_relations
## declared args: 
def dash_relations(request, *args, **kwargs):
    """dash_relations() returns ..."""
    s = {}
    return render_to_response('dash/relations.html', s)

## rest: GET /ui/dash/search.html
## function: dash_search
## declared args: 
def dash_search(request, *args, **kwargs):
    """dash_search() returns ..."""
    s = {}
    return render_to_response('dash/search.html', s)

## rest: GET /ui/dash/tags.html
## function: dash_tags
## declared args: 
def dash_tags(request, *args, **kwargs):
    """dash_tags() returns ..."""
    s = {}
    return render_to_response('dash/tags.html', s)

## rest: GET /ui/dash/vurls.html
## function: dash_vurls
## declared args: 
def dash_vurls(request, *args, **kwargs):
    """dash_vurls() returns ..."""
    s = {}
    return render_to_response('dash/vurls.html', s)

## rest: GET /ui/delete/comment/CID.html
## function: delete_comment
## declared args: cid
def delete_comment(request, cid, *args, **kwargs):
    """delete_comment(cid) returns ..."""
    s = {'commentId': cid}
    return render_to_response('delete/comment.html', s)

## rest: GET /ui/delete/item/IID.html
## function: delete_item
## declared args: iid
def delete_item(request, iid, *args, **kwargs):
    """delete_item(iid) returns ..."""
    s = {'itemId': iid}
    return render_to_response('delete/item.html', s)

## rest: GET /ui/delete/relation/RID.html
## function: delete_relation
## declared args: rid
def delete_relation(request, rid, *args, **kwargs):
    """delete_relation(rid) returns ..."""
    s = {'relationId': rid}
    return render_to_response('delete/relation.html', s)

## rest: GET /ui/delete/tag/TID.html
## function: delete_tag
## declared args: tid
def delete_tag(request, tid, *args, **kwargs):
    """delete_tag(tid) returns ..."""
    s = {'tagId': tid}
    return render_to_response('delete/tag.html', s)

## rest: GET /ui/delete/vurl/VID.html
## function: delete_vurl
## declared args: vid
def delete_vurl(request, vid, *args, **kwargs):
    """delete_vurl(vid) returns ..."""
    s = {'vurlId': vid}
    return render_to_response('delete/vurl.html', s)

## rest: GET /ui/list/comments/IID.html
## function: list_comments
## declared args: iid
def list_comments(request, iid, *args, **kwargs):
    """list_comments(iid) returns ..."""
    s = api.list_comments(request, iid, *args, **kwargs)
    s['itemId'] = iid # HACK TO SUPPORT PAGE
    return render_to_response('list/comments.html', s)

## rest: GET /ui/list/items.html
## function: list_items
## declared args: 
def list_items(request, *args, **kwargs):
    """list_items() returns ..."""
    s = api.list_items(request, *args, **kwargs)
    return render_to_response('list/items.html', s)

## rest: GET /ui/list/relations.html
## function: list_relations
## declared args: 
def list_relations(request, *args, **kwargs):
    """list_relations() returns ..."""
    s = api.list_relations(request, *args, **kwargs)
    return render_to_response('list/relations.html', s)

## rest: GET /ui/list/tags.html
## function: list_tags
## declared args: 
def list_tags(request, *args, **kwargs):
    """list_tags() returns ..."""
    s = api.list_tags(request, *args, **kwargs)
    return render_to_response('list/tags.html', s)

## rest: GET /ui/list/vurls.html
## function: list_vurls
## declared args: 
def list_vurls(request, *args, **kwargs):
    """list_vurls() returns ..."""
    s = api.list_vurls(request, *args, **kwargs)
    return render_to_response('list/vurls.html', s)

## rest: GET /ui/read/comment/CID.html
## function: read_comment
## declared args: cid
def read_comment(request, cid, *args, **kwargs):
    """read_comment(cid) returns ..."""
    s = api.read_comment(request, cid, *args, **kwargs)
    return render_to_response('read/comment.html', s)

## rest: GET /ui/read/item/IID.html
## function: read_item
## declared args: iid
def read_item(request, iid, *args, **kwargs):
    """read_item(iid) returns ..."""
    s = api.read_item(request, iid, *args, **kwargs)
    return render_to_response('read/item.html', s)

## rest: GET /ui/read/relation/RID.html
## function: read_relation
## declared args: rid
def read_relation(request, rid, *args, **kwargs):
    """read_relation(rid) returns ..."""
    s = api.read_relation(request, rid, *args, **kwargs)
    return render_to_response('read/relation.html', s)

## rest: GET /ui/read/tag/TID.html
## function: read_tag
## declared args: tid
def read_tag(request, tid, *args, **kwargs):
    """read_tag(tid) returns ..."""
    s = api.read_tag(request, tid, *args, **kwargs)
    return render_to_response('read/tag.html', s)

## rest: GET /ui/read/vurl/VID.html
## function: read_vurl
## declared args: vid
def read_vurl(request, vid, *args, **kwargs):
    """read_vurl(vid) returns ..."""
    s = api.read_vurl(request, vid, *args, **kwargs)
    return render_to_response('read/vurl.html', s)

## rest: GET /ui/search/comments.html
## function: search_comments
## declared args: 
def search_comments(request, *args, **kwargs):
    """search_comments() returns ..."""
    s = {}
    return render_to_response('search/comments.html', s)

## rest: GET /ui/search/items.html
## function: search_items
## declared args: 
def search_items(request, *args, **kwargs):
    """search_items() returns ..."""
    s = {}
    return render_to_response('search/items.html', s)

## rest: GET /ui/search/relations.html
## function: search_relations
## declared args: 
def search_relations(request, *args, **kwargs):
    """search_relations() returns ..."""
    s = {}
    return render_to_response('search/relations.html', s)

## rest: GET /ui/search/tags.html
## function: search_tags
## declared args: 
def search_tags(request, *args, **kwargs):
    """search_tags() returns ..."""
    s = {}
    return render_to_response('search/tags.html', s)

## rest: GET /ui/search/vurls.html
## function: search_vurls
## declared args: 
def search_vurls(request, *args, **kwargs):
    """search_vurls() returns ..."""
    s = {}
    return render_to_response('search/vurls.html', s)

## rest: GET /ui/update/comment/CID.html
## function: update_comment
## declared args: cid
def update_comment(request, cid, *args, **kwargs):
    """update_comment(cid) returns ..."""
    s = Comment.objects.get(id=cid).to_structure()
    return render_to_response('update/comment.html', s)

## rest: GET /ui/update/item/IID.html
## function: update_item
## declared args: iid
def update_item(request, iid, *args, **kwargs):
    """update_item(iid) returns ..."""
    s = Item.objects.get(id=iid).to_structure()
    return render_to_response('update/item.html', s)

## rest: GET /ui/update/relation/RID.html
## function: update_relation
## declared args: rid
def update_relation(request, rid, *args, **kwargs):
    """update_relation(rid) returns ..."""
    s = Relation.objects.get(id=rid).to_structure()
    return render_to_response('update/relation.html', s)

## rest: GET /ui/update/tag/TID.html
## function: update_tag
## declared args: tid
def update_tag(request, tid, *args, **kwargs):
    """update_tag(tid) returns ..."""
    s = Tag.objects.get(id=tid).to_structure()
    return render_to_response('update/tag.html', s)

## rest: GET /ui/update/vurl/VID.html
## function: update_vurl
## declared args: vid
def update_vurl(request, vid, *args, **kwargs):
    """update_vurl(vid) returns ..."""
    s = Vurl.objects.get(id=vid).to_structure()
    return render_to_response('update/vurl.html', s)

## rest: GET /ui/version.html
## function: read_version
## declared args: 
def read_version(request, *args, **kwargs):
    """read_version() returns ..."""
    s = api.read_version(request, *args, **kwargs)
    return render_to_response('read/version.html', s)

