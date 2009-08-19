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

from django.core import serializers
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404

from mine.models import Tag, Item, Relation, Comment
from mine.models import request_to_model_and_save

#from pymine.tools.io import FileBlockIterator

def api_retval(data=None, **kwargs):
    template = {}
    if data: template['data'] = data
    template['exit'] = kwargs.get('exit', 0)
    template['status'] = kwargs.get('status', 'ok')
    # ... prevpage, nextpage, thispage, callback, maxcount, watchdog...
    return template

##################################################################

## rest: GET /api
## function: read_api_root
## declared args: 
def read_api_root(request, *args, **kwargs):
    return render_to_response('read-api-root.html') ### THIS ROUTINE IS FILTERED THRU 'REST()' NOT 'API_CALL()'

## rest: GET /api/item/IID
## function: read_item_data
## declared args: iid
def read_item_data(request, iid, *args, **kwargs):
    id = int(iid)
    m = Item.objects.get(id=id)
    f = m.data.chunks()
    ct = m.content_type
    return HttpResponse(f, mimetype=ct) ### THIS ROUTINE IS FILTERED THRU 'REST()' NOT 'API_CALL()'

## rest: GET /api/item.FMT
## function: read_item_list
## declared args: 
def read_item_list(request, *args, **kwargs):
    return api_retval()

## rest: POST /api/item.FMT
## function: create_item
## declared args: 
def create_item(request, *args, **kwargs):
    m = request_to_model_and_save('item', request)
    return api_retval(m.structure()) 

## rest: DELETE /api/item/IID.FMT
## function: delete_item
## declared args: iid
def delete_item(request, iid, *args, **kwargs):
    return api_retval()

## rest: GET /api/item/IID.FMT
## function: read_item
## declared args: iid
def read_item(request, iid, *args, **kwargs):
    id = int(iid)
    m = Item.objects.get(id=id)
    return api_retval(m.structure())

## rest: POST /api/item/IID.FMT
## function: update_item
## declared args: iid
def update_item(request, iid, *args, **kwargs):
    return api_retval()

## rest: DELETE /api/item/IID/key/KEY.FMT
## function: delete_item_key
## declared args: iid key
def delete_item_key(request, iid, key, *args, **kwargs):
    return api_retval()

## rest: GET /api/item/IID/key/KEY.FMT
## function: get_item_key
## declared args: iid key
def get_item_key(request, iid, key, *args, **kwargs):
    return api_retval()

## rest: GET /api/relation.FMT
## function: read_relation_list
## declared args: 
def read_relation_list(request, *args, **kwargs):
    return api_retval()

## rest: POST /api/relation.FMT
## function: create_relation
## declared args: 
def create_relation(request, *args, **kwargs):
    m = request_to_model_and_save('relation', request)
    return api_retval(m.structure()) 

## rest: DELETE /api/relation/RID.FMT
## function: delete_relation
## declared args: rid
def delete_relation(request, rid, *args, **kwargs):
    return api_retval()

## rest: GET /api/relation/RID.FMT
## function: read_relation
## declared args: rid
def read_relation(request, rid, *args, **kwargs):
    id = int(rid)
    m = Relation.objects.get(id=id)
    return api_retval(m.structure())

## rest: POST /api/relation/RID.FMT
## function: update_relation
## declared args: rid
def update_relation(request, rid, *args, **kwargs):
    return api_retval()

## rest: DELETE /api/relation/RID/key/KEY.FMT
## function: delete_relation_key
## declared args: rid key
def delete_relation_key(request, rid, key, *args, **kwargs):
    return api_retval()

## rest: GET /api/relation/RID/key/KEY.FMT
## function: get_relation_key
## declared args: rid key
def get_relation_key(request, rid, key, *args, **kwargs):
    return api_retval()

## rest: GET /api/tag.FMT
## function: read_tag_list
## declared args: 
def read_tag_list(request, *args, **kwargs):
    return api_retval()

## rest: POST /api/tag.FMT
## function: create_tag
## declared args: 
def create_tag(request, *args, **kwargs):
    m = request_to_model_and_save('tag', request)
    return api_retval(m.structure()) 

## rest: DELETE /api/tag/TID.FMT
## function: delete_tag
## declared args: tid
def delete_tag(request, tid, *args, **kwargs):
    return api_retval()

## rest: GET /api/tag/TID.FMT
## function: read_tag
## declared args: tid
def read_tag(request, tid, *args, **kwargs):
    id = int(tid)
    m = Tag.objects.get(id=id)
    return api_retval(m.structure())

## rest: POST /api/tag/TID.FMT
## function: update_tag
## declared args: tid
def update_tag(request, tid, *args, **kwargs):
    return api_retval()

## rest: DELETE /api/tag/TID/key/KEY.FMT
## function: delete_tag_key
## declared args: tid key
def delete_tag_key(request, tid, key, *args, **kwargs):
    return api_retval()

## rest: GET /api/tag/TID/key/KEY.FMT
## function: get_tag_key
## declared args: tid key
def get_tag_key(request, tid, key, *args, **kwargs):
    return api_retval()

## rest: GET /api/item/IID/comment.FMT
## function: read_comment_list
## declared args: iid
def read_comment_list(request, iid, *args, **kwargs):
    return api_retval()

## rest: POST /api/item/IID/comment.FMT
## function: create_comment
## declared args: iid
def create_comment(request, iid, *args, **kwargs):
    return api_retval()

## rest: DELETE /api/item/IID/CID.FMT
## function: delete_comment
## declared args: iid cid
def delete_comment(request, iid, cid, *args, **kwargs):
    return api_retval()

## rest: GET /api/item/IID/CID.FMT
## function: read_comment
## declared args: iid cid
def read_comment(request, iid, cid, *args, **kwargs):
    return api_retval()

## rest: POST /api/item/IID/CID.FMT
## function: update_comment
## declared args: iid cid
def update_comment(request, iid, cid, *args, **kwargs):
    return api_retval()

## rest: DELETE /api/item/IID/CID/key/KEY.FMT
## function: delete_comment_key
## declared args: iid cid key
def delete_comment_key(request, iid, cid, key, *args, **kwargs):
    return api_retval()

## rest: GET /api/item/IID/CID/key/KEY.FMT
## function: get_comment_key
## declared args: iid cid key
def get_comment_key(request, iid, cid, key, *args, **kwargs):
    return api_retval()

## rest: GET /api/item/IID/clone.FMT
## function: read_clone_list
## declared args: iid
def read_clone_list(request, iid, *args, **kwargs):
    return api_retval()

## rest: POST /api/item/IID/clone.FMT
## function: create_clone
## declared args: iid
def create_clone(request, iid, *args, **kwargs):
    return api_retval()

## rest: GET /api/registry.FMT
## function: read_registry
## declared args: 
def read_registry(request, *args, **kwargs):
    return api_retval()

## rest: POST /api/registry.FMT
## function: update_registry
## declared args: 
def update_registry(request, *args, **kwargs):
    return api_retval()

## rest: DELETE /api/registry/key/KEY.FMT
## function: delete_registry_key
## declared args: key
def delete_registry_key(request, key, *args, **kwargs):
    return api_retval()

## rest: GET /api/registry/key/KEY.FMT
## function: get_registry_key
## declared args: key
def get_registry_key(request, key, *args, **kwargs):
    return api_retval()

## rest: GET /api/select/item.FMT
## function: read_select_item
## declared args: 
def read_select_item(request, *args, **kwargs):
    return api_retval()

## rest: GET /api/select/relation.FMT
## function: read_select_relation
## declared args: 
def read_select_relation(request, *args, **kwargs):
    return api_retval()

## rest: GET /api/select/tag.FMT
## function: read_select_tag
## declared args: 
def read_select_tag(request, *args, **kwargs):
    return api_retval()

## rest: GET /api/url/RID.FMT
## function: encode_minekey1
## declared args: rid
def encode_minekey1(request, rid, *args, **kwargs):
    # CHAIN TO encode_minekey2
    return api_retval()

## rest: GET /api/url/RID/IID.FMT
## function: encode_minekey2
## declared args: rid iid
def encode_minekey2(request, rid, iid, *args, **kwargs):
    # CHAIN TO encode_minekey3
    return api_retval()

## rest: GET /api/url/RID/RVSN/IID.FMT
## function: encode_minekey3
## declared args: rid rvsn iid
def encode_minekey3(request, rid, rvsn, iid, *args, **kwargs):
    return api_retval()

## rest: GET /api/version.FMT
## function: read_version
## declared args: 
def read_version(request, *args, **kwargs):
    data = { 
        'softwareName': 'pymine',
        'softwareRevision': '1.0-alpha',
        'mineAPIVersion': 2,
        }
    return api_retval(data)
