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

def api_retval(result=None, **kwargs):
    template = {}
    if result: template['result'] = result
    template['status'] = kwargs.get('status', 'ok')
    template['exit'] = kwargs.get('exit', 0)

    for k in ( 'prevurl', 'nexturl', 'thisurl',
	       'thissize', 'totalsize',
	       'callback', 'watch' ):
	v = kwargs.get(k)
	if v:
	    template[k] = v
    return template

def list_foos(model):
    result = [ m.to_structure() for m in model.objects.all() ]
    return api_retval(result, totalsize=len(result))

def create_foo(model, request):
    m = model.new_from_request(request)
    return api_retval(m.to_structure())

def delete_foo(model, mid):
    m = model.objects.get(id=int(mid))
    m.delete()
    return api_retval()

def read_foo(model, mid):
    m = model.objects.get(id=int(mid))
    return api_retval(m.to_structure())

def update_foo(model, request, mid):
    m = model.objects.get(id=int(mid))
    m.update_from_request(request)
    return api_retval(m.to_structure())

def delete_foo_key(model, id, sattr):
    m = model.objects.get(id=int(mid))
    m.delete_sattr(sattr)
    return api_retval(m.to_structure())

def get_foo_key(model, id, sattr):
    m = model.objects.get(id=int(mid))
    s = m.to_structure()
    if not sattr in s:
	raise Exception, "sattr not found: " + sattr
    return api_retval(s[sattr])

##################################################################
##################################################################
##################################################################

## rest: GET /api
## function: read_api_root
## declared args:
def read_api_root(request, *args, **kwargs):
    """REST function that handles the template for the root api directory"""
    return render_to_response('read-api-root.html')

## rest: GET /api/item/IID
## function: read_item_data
## declared args: iid
def read_item_data(request, iid, *args, **kwargs):
    """REST function that handles the retreival of actual item data, eg JPEG files"""
    id = int(iid)
    m = Item.objects.get(id=id)
    f = m.data.chunks()
    ct = m.content_type
    return HttpResponse(f, mimetype=ct)

##################################################################

## rest: GET /api/item.FMT
## function: list_items
## declared args:
def list_items(request, *args, **kwargs):
    return list_foos(Item)

## rest: POST /api/item.FMT
## function: create_item
## declared args:
def create_item(request, *args, **kwargs):
    return create_foo(Item, request)

## rest: DELETE /api/item/IID.FMT
## function: delete_item
## declared args: iid
def delete_item(request, iid, *args, **kwargs):
    return delete_foo(Item, iid)

## rest: GET /api/item/IID.FMT
## function: read_item
## declared args: iid
def read_item(request, iid, *args, **kwargs):
    return read_foo(Item, iid)

## rest: POST /api/item/IID.FMT
## function: update_item
## declared args: iid
def update_item(request, iid, *args, **kwargs):
    return update_foo(Item, request, iid)

## rest: DELETE /api/item/IID/KEY.FMT
## function: delete_item_key
## declared args: iid key
def delete_item_key(request, iid, key, *args, **kwargs):
    return delete_foo_key(Item, iid, key)

## rest: GET /api/item/IID/KEY.FMT
## function: get_item_key
## declared args: iid key
def get_item_key(request, iid, key, *args, **kwargs):
    return get_foo_key(Item, iid, key)

##################################################################

## rest: GET /api/relation.FMT
## function: list_relations
## declared args:
def list_relations(request, *args, **kwargs):
    return list_foos(Relation)

## rest: POST /api/relation.FMT
## function: create_relation
## declared args:
def create_relation(request, *args, **kwargs):
    return create_foo(Relation, request)

## rest: DELETE /api/relation/RID.FMT
## function: delete_relation
## declared args: rid
def delete_relation(request, rid, *args, **kwargs):
    return delete_foo(Relation, rid)

## rest: GET /api/relation/RID.FMT
## function: read_relation
## declared args: rid
def read_relation(request, rid, *args, **kwargs):
    return read_foo(Relation, rid)

## rest: POST /api/relation/RID.FMT
## function: update_relation
## declared args: rid
def update_relation(request, rid, *args, **kwargs):
    return update_foo(Relation, request, rid)

## rest: DELETE /api/relation/RID/KEY.FMT
## function: delete_relation_key
## declared args: rid key
def delete_relation_key(request, rid, key, *args, **kwargs):
    return delete_foo_key(Relation, rid, key)

## rest: GET /api/relation/RID/KEY.FMT
## function: get_relation_key
## declared args: rid key
def get_relation_key(request, rid, key, *args, **kwargs):
    return get_foo_key(Relation, rid, key)

##################################################################

## rest: GET /api/tag.FMT
## function: list_tags
## declared args:
def list_tags(request, *args, **kwargs):
    return list_foos(Tag)

## rest: POST /api/tag.FMT
## function: create_tag
## declared args:
def create_tag(request, *args, **kwargs):
    return create_foo(Tag, request)

## rest: DELETE /api/tag/TID.FMT
## function: delete_tag
## declared args: tid
def delete_tag(request, tid, *args, **kwargs):
    return delete_foo(Tag, tid)

## rest: GET /api/tag/TID.FMT
## function: read_tag
## declared args: tid
def read_tag(request, tid, *args, **kwargs):
    return read_foo(Tag, tid)

## rest: POST /api/tag/TID.FMT
## function: update_tag
## declared args: tid
def update_tag(request, tid, *args, **kwargs):
    return update_foo(Tag, request, tid)

## rest: DELETE /api/tag/TID/KEY.FMT
## function: delete_tag_key
## declared args: tid key
def delete_tag_key(request, tid, key, *args, **kwargs):
    return delete_foo_key(Tag, tid, key)

## rest: GET /api/tag/TID/KEY.FMT
## function: get_tag_key
## declared args: tid key
def get_tag_key(request, tid, key, *args, **kwargs):
    return get_foo_key(Tag, tid, key)

##################################################################

## rest: GET /api/comment/item/IID.FMT
## function: list_comments
## declared args: iid
def list_comments(request, iid, *args, **kwargs):
    item_id = int(iid)
    if item_id == 0:
        result = [ m.to_structure() for m in Comment.objects.all() ]
    else:
        result = [ m.to_structure() for m in Comment.objects.filter(item=Item.objects.get(id=item_id)) ]
    return api_retval(result, totalsize=len(result))

## rest: POST /api/comment/item/IID.FMT
## function: create_comment
## declared args: iid
def create_comment(request, iid, *args, **kwargs):
    m = request_to_model_and_save(Comment, request)
    return api_retval(m.to_structure())

## rest: DELETE /api/comment/CID.FMT
## function: delete_comment
## declared args: cid
def delete_comment(request, cid, *args, **kwargs):
    return delete_foo(Comment, cid)

## rest: GET /api/comment/CID.FMT
## function: read_comment
## declared args: cid
def read_comment(request, cid, *args, **kwargs):
    return read_foo(Comment, cid)

## rest: POST /api/comment/CID.FMT
## function: update_comment
## declared args: cid
def update_comment(request, cid, *args, **kwargs):
    return update_foo(Comment, request, cid)

## rest: DELETE /api/comment/CID/KEY.FMT
## function: delete_comment_key
## declared args: cid key
def delete_comment_key(request, cid, key, *args, **kwargs):
    return delete_foo_key(Comment, cid, key)

## rest: GET /api/comment/CID/KEY.FMT
## function: get_comment_key
## declared args: cid key
def get_comment_key(request, cid, key, *args, **kwargs):
    return get_foo_key(Comment, cid, key)

##################################################################

## rest: GET /api/clone/IID.FMT
## function: list_clones
## declared args: iid
def list_clones(request, iid, *args, **kwargs):
    return api_retval()

## rest: POST /api/clone/IID.FMT
## function: create_clone
## declared args: iid
def create_clone(request, iid, *args, **kwargs):
    return api_retval()

##################################################################

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

## rest: DELETE /api/registry/KEY.FMT
## function: delete_registry_key
## declared args: key
def delete_registry_key(request, key, *args, **kwargs):
    return api_retval()

## rest: GET /api/registry/KEY.FMT
## function: get_registry_key
## declared args: key
def get_registry_key(request, key, *args, **kwargs):
    return api_retval()

##################################################################

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

##################################################################

## rest: GET /api/url/RID.FMT
## function: encode_minekey1
## declared args: rid
def encode_minekey1(request, rid, *args, **kwargs):
    """return the MineKey for overall feed for Relation RID with current RVSN"""
    return encode_minekey2(request, rid, 0, *args, **kwargs)

## rest: GET /api/url/RID/IID.FMT
## function: encode_minekey2
## declared args: rid iid
def encode_minekey2(request, rid, iid, *args, **kwargs):
    """return the MineKey for Item IID for Relation RID with current RVSN"""
    return encode_minekey3(request, rid, 0, iid, *args, **kwargs)

## rest: GET /api/url/RID/RVSN/IID.FMT
## function: encode_minekey3
## declared args: rid rvsn iid
def encode_minekey3(request, rid, rvsn, iid, *args, **kwargs):
    """return the MineKey for Item IID for Relation RID with given RVSN"""
    if rvsn == 0:
        # go look it up
        pass
    
    result = { 
        'keyversion': 'fake',
        'method': 'fake',
        'iid': iid,
        'rid': rid,
        'rvsn': rvsn,
        'depth': 'fake',
        }

    return api_retval(result)

##################################################################

## rest: GET /api/version.FMT
## function: read_version
## declared args:
def read_version(request, *args, **kwargs):
    result = {
	'softwareName': 'pymine',
	'softwareRevision': '1.0-alpha',
	'mineAPIVersion': 2,
	}
    return api_retval(result)

##################################################################
##################################################################
##################################################################
