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

from django.conf import settings
from django.core import serializers
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404

from models import Tag, Item, Relation, Comment, Vurl, Registry

def construct_retval(request, result, **kwargs):
    """
    constructs an 'envelope' structure around the results of an API
    call, providing metainformation to be rendered into XML, JSON, etc

    request may be None

    result may be None
    """

    template = {}

    template['exit'] = kwargs.get('exit', 0)
    template['status'] = kwargs.get('status', 'ok')

    if result: 
        template['result'] = result

    # inputs:
    # query (dealt with elsewhere)
    # span (pagination off, if zero)
    # page (ie: desired)

    # outputs:
    # page (ie: current)
    # query (ie: same as input)
    # span
    # first
    # prev
    # next
    # last
    # firsturl
    # prevurl
    # nexturl
    # lasturl

    return template

def create_foo(request, model):
    """
    """

    m = model.new_from_request(request)
    return construct_retval(request, m.to_structure())

def delete_foo(request, model, mid):
    """
    """

    m = model.objects.get(id=int(mid))
    m.delete()
    return construct_retval(request, None)

def read_foo(request, model, mid):
    """
    """

    m = model.objects.get(id=int(mid))
    return construct_retval(request, m.to_structure())

def update_foo(request, model, mid):
    """
    """

    m = model.objects.get(id=int(mid))
    m = m.update_from_request(request)
    return construct_retval(request, m.to_structure())

def delete_foo_key(model, mid, sattr):
    """
    """

    m = model.objects.get(id=int(mid))
    m.delete_sattr(sattr)
    return construct_retval(request, m.to_structure())

def get_foo_key(model, mid, sattr):
    """
    """

    m = model.objects.get(id=int(mid))
    s = m.to_structure()
    if not sattr in s:
	raise RuntimeError, "sattr not found: " + sattr
    return construct_retval(request, s[sattr])

def nyi():
    """
    """

    raise RuntimeException, 'not yet implemented'

##################################################################
##################################################################
##################################################################

## function: delete_comment
## declared args: cid
def delete_comment(request, cid, *args, **kwargs):
    """delete_comment(cid) returns ..."""
    return delete_foo(request, Comment, cid)

## rest: GET /api/comment/CID.FMT
## function: read_comment
## declared args: cid
def read_comment(request, cid, *args, **kwargs):
    """read_comment(cid) returns ..."""
    return read_foo(request, Comment, cid)

## rest: POST /api/comment/CID.FMT
## function: update_comment
## declared args: cid
def update_comment(request, cid, *args, **kwargs):
    """update_comment(cid) returns ..."""
    return update_foo(request, Comment, cid)

## function: delete_comment_key
## declared args: cid sattr
def delete_comment_key(request, cid, sattr, *args, **kwargs):
    """delete_comment_key(cid, sattr) returns ..."""
    return delete_foo_key(Comment, cid, sattr)

## rest: GET /api/comment/CID/SATTR.FMT
## function: get_comment_key
## declared args: cid sattr
def get_comment_key(request, cid, sattr, *args, **kwargs):
    """get_comment_key(cid, sattr) returns ..."""
    return get_foo_key(Comment, cid, sattr)

## rest: POST /api/comment/item/IID.FMT
## function: create_comment
## declared args: iid
def create_comment(request, iid, *args, **kwargs):
    """create_comment(iid) returns ..."""
    m = Comment.new_from_request(request, commentItemId=int(iid)) # use kwargs to push extra information
    return construct_retval(request, m.to_structure())

## rest: GET /api/comment/item/IID.FMT
## function: list_comments
## declared args: iid
def list_comments(request, iid, *args, **kwargs):
    """list_comments(iid) returns ..."""
    item_id = int(iid)

    if item_id == 0:
        models = Comment.objects
    else:
        item = Item.objects.get(id=item_id)
        models = item.comment_set

    qs = models.filter(is_deleted=False)

    if 'query' in request.REQUEST:
        qs = Comment.filter_queryset(qs, request.REQUEST['query'])

    result = [ { m.sattr_prefix : m.to_structure() } for m in qs ]
    return construct_retval(request, result)

##################################################################

## rest: GET /api/ie/export.EFMT
## function: export_mine
## declared args: efmt
def export_mine(request, efmt, *args, **kwargs):
    """export_mine(efmt) returns ..."""
    nyi()

## rest: GET /api/ie/import.EFMT
## function: import_mine
## declared args: efmt
def import_mine(request, efmt, *args, **kwargs):
    """import_mine(efmt) returns ..."""
    nyi()

##################################################################

## rest: POST /api/item.FMT
## function: create_item
## declared args: 
def create_item(request, *args, **kwargs):
    """create_item() returns ..."""
    return create_foo(request, Item)

## rest: GET /api/item.FMT
## function: list_items
## declared args: 
def list_items(request, *args, **kwargs):
    """list_items() returns ..."""
    qs = Item.objects.filter(is_deleted=False)

    if 'query' in request.REQUEST:
        qs = Item.filter_queryset(qs, request.REQUEST['query'])

    result = [ { m.sattr_prefix : m.to_structure() } for m in qs ]
    return construct_retval(request, result)


## rest: GET /api/item/IID
## function: read_item_data
## declared args: iid
def read_item_data(request, iid, *args, **kwargs): # <--------------------------------- THE BIG ONE
    """read_item_data(iid) handles the retreival of actual item data, eg JPEG files"""

    mk = kwargs.get('minekey', None)

    if mk and mk.iid == iid:
        m = mk.get_item()
    else:
        m = Item.objects.get(id=int(iid))

    ct = m.item_type()

    # if we can have context and we can rewrite
    if mk and ct in ('text/html', 'application/mine+xml'): 
        if m.data:
            content = m.data.read()
        else:
            content = m.item_feed_description()

        rewrite = mk.rewrite_html(content)
        response = HttpResponse(rewrite, content_type=ct)
        response['Content-Length'] = len(rewrite)

    elif m.data: # else if there's a file
        fw = m.data.chunks()
        response = HttpResponse(fw, content_type=ct)
        response['Content-Length'] = m.data.size

    else: # default
        response = HttpResponse(m.item_feed_description(), content_type=ct)
        response['Content-Length'] = m.item_size()

    return response

## function: delete_item
## declared args: iid
def delete_item(request, iid, *args, **kwargs):
    """delete_item(iid) returns ..."""
    return delete_foo(request, Item, iid)

## rest: GET /api/item/IID.FMT
## function: read_item
## declared args: iid
def read_item(request, iid, *args, **kwargs):
    """read_item(iid) returns ..."""
    return read_foo(request, Item, iid)

## rest: POST /api/item/IID.FMT
## function: update_item
## declared args: iid
def update_item(request, iid, *args, **kwargs):
    """update_item(iid) returns ..."""
    return update_foo(request, Item, iid)

## function: delete_item_key
## declared args: iid sattr
def delete_item_key(request, iid, sattr, *args, **kwargs):
    """delete_item_key(iid, sattr) returns ..."""
    return delete_foo_key(Item, iid, sattr)

## rest: GET /api/item/IID/SATTR.FMT
## function: get_item_key
## declared args: iid sattr
def get_item_key(request, iid, sattr, *args, **kwargs):
    """get_item_key(iid, sattr) returns ..."""
    return get_foo_key(Item, iid, sattr)

##################################################################

# TBD: REGISTRY SECURITY

# at some point in the future we will require setting of anything
# where key begins with "__" over a POST and SSL connection.

# in the future we will refuse to return anything beginning with "__"
# at *all*

# if we permitted deletion via primary-key (eg: delete where id=42) in
# *addition* to deletion by name, then we would have to
# duplicate/replicate a bunch of security checks and it could get
# awkward.  So, we delete from the registry by keyname alone, that way
# you are more likely to GWYW / GWYAF

## rest: GET /api/registry.FMT
## function: list_registry
## declared args: 
def list_registry(request, *args, **kwargs):
    """list_registry() returns ..."""
    qs = Registry.objects.all()
    result = [ m.to_structure() for m in qs ]
    return construct_retval(request, result)

## rest: POST /api/registry/RATTR.FMT
## function: amend_registry_key
## declared args: rattr
def amend_registry_key(request, rattr, *args, **kwargs):
    """amend_registry_key(rattr) returns ..."""
    v = request.POST[rattr]
    m, created = Registry.objects.get_or_create(key=rattr, defaults={ 'value': v })
    if not created: # then it will need updating
        m.value = v
        m.save();
    return construct_retval(request, m.to_structure())

## function: delete_registry_key
## declared args: rattr
def delete_registry_key(request, rattr, *args, **kwargs):
    """delete_registry_key(rattr) returns ..."""
    m = Registry.objects.get(key=rattr)
    m.delete()
    return construct_retval(request, None)

## rest: GET /api/registry/RATTR.FMT
## function: get_registry_key
## declared args: rattr
def get_registry_key(request, rattr, *args, **kwargs):
    """get_registry_key(rattr) returns ..."""
    m = Registry.objects.get(key=rattr)
    return construct_retval(request, m.value)

##################################################################

## rest: POST /api/relation.FMT
## function: create_relation
## declared args: 
def create_relation(request, *args, **kwargs):
    """create_relation() returns ..."""
    return create_foo(request, Relation)

## rest: GET /api/relation.FMT
## function: list_relations
## declared args: 
def list_relations(request, *args, **kwargs):
    """list_relations() returns ..."""
    qs = Relation.objects.filter(is_deleted=False)

    if 'query' in request.REQUEST:
        qs = Relation.filter_queryset(qs, request.REQUEST['query'])

    result = [ { m.sattr_prefix : m.to_structure() } for m in qs ]
    return construct_retval(request, result)

## function: delete_relation
## declared args: rid
def delete_relation(request, rid, *args, **kwargs):
    """delete_relation(rid) returns ..."""
    return delete_foo(request, Relation, rid)

## rest: GET /api/relation/RID.FMT
## function: read_relation
## declared args: rid
def read_relation(request, rid, *args, **kwargs):
    """read_relation(rid) returns ..."""
    return read_foo(request, Relation, rid)

## rest: POST /api/relation/RID.FMT
## function: update_relation
## declared args: rid
def update_relation(request, rid, *args, **kwargs):
    """update_relation(rid) returns ..."""
    return update_foo(request, Relation, rid)

## function: delete_relation_key
## declared args: rid sattr
def delete_relation_key(request, rid, sattr, *args, **kwargs):
    """delete_relation_key(rid, sattr) returns ..."""
    return delete_foo_key(Relation, rid, sattr)

## rest: GET /api/relation/RID/SATTR.FMT
## function: get_relation_key
## declared args: rid sattr
def get_relation_key(request, rid, sattr, *args, **kwargs):
    """get_relation_key(rid, sattr) returns ..."""
    return get_foo_key(Relation, rid, sattr)

##################################################################

## rest: POST /api/tag.FMT
## function: create_tag
## declared args: 
def create_tag(request, *args, **kwargs):
    """create_tag() returns ..."""
    return create_foo(request, Tag)

## rest: GET /api/tag.FMT
## function: list_tags
## declared args: 
def list_tags(request, *args, **kwargs):
    """list_tags() returns ..."""
    qs = Tag.objects.filter(is_deleted=False)

    if 'query' in request.REQUEST:
        qs = Tag.filter_queryset(qs, request.REQUEST['query'])

    result = [ { m.sattr_prefix : m.to_structure() } for m in qs ]
    return construct_retval(request, result)

## function: delete_tag
## declared args: tid
def delete_tag(request, tid, *args, **kwargs):
    """delete_tag(tid) returns ..."""
    return delete_foo(request, Tag, tid)

## rest: GET /api/tag/TID.FMT
## function: read_tag
## declared args: tid
def read_tag(request, tid, *args, **kwargs):
    """read_tag(tid) returns ..."""
    return read_foo(request, Tag, tid)

## rest: POST /api/tag/TID.FMT
## function: update_tag
## declared args: tid
def update_tag(request, tid, *args, **kwargs):
    """update_tag(tid) returns ..."""
    return update_foo(request, Tag, tid)

## function: delete_tag_key
## declared args: tid sattr
def delete_tag_key(request, tid, sattr, *args, **kwargs):
    """delete_tag_key(tid, sattr) returns ..."""
    return delete_foo_key(Tag, tid, sattr)

## rest: GET /api/tag/TID/SATTR.FMT
## function: get_tag_key
## declared args: tid sattr
def get_tag_key(request, tid, sattr, *args, **kwargs):
    """get_tag_key(tid, sattr) returns ..."""
    return get_foo_key(Tag, tid, sattr)

##################################################################

## rest: GET /api/url/RID.FMT
## function: encode_minekey1
## declared args: rid
def encode_minekey1(request, rid, *args, **kwargs):
    """encode_minekey1(rid) returns ..."""
    nyi() 

## rest: GET /api/url/RID/IID.FMT
## function: encode_minekey2
## declared args: rid iid
def encode_minekey2(request, rid, iid, *args, **kwargs):
    """encode_minekey2(rid, iid) returns ..."""
    nyi() 

## rest: GET /api/url/RID/RVSN/IID.FMT
## function: encode_minekey3
## declared args: rid rvsn iid
def encode_minekey3(request, rid, rvsn, iid, *args, **kwargs):
    """encode_minekey3(rid, rvsn, iid) returns ..."""
    nyi() 

##################################################################

## rest: GET /api/version.FMT
## function: read_version
## declared args: 
def read_version(request, *args, **kwargs):
    """read_version() returns ..."""
    result = {
        'softwareName': settings.MINE_SOFTWARE_NAME,
        'softwareRevision': settings.MINE_SOFTWARE_VERSION,
        'mineApiVersion': settings.MINE_API_VERSION,
        }
    return construct_retval(request, result)

##################################################################

## rest: POST /api/vurl.FMT
## function: create_vurl
## declared args: 
def create_vurl(request, *args, **kwargs):
    """create_vurl() returns ..."""
    return create_foo(request, Vurl)

## rest: GET /api/vurl.FMT
## function: list_vurls
## declared args: 
def list_vurls(request, *args, **kwargs):
    """list_vurls() returns ..."""
    qs = Vurl.objects.filter(is_deleted=False)

    if 'query' in request.REQUEST:
        qs = Vurl.filter_queryset(qs, request.REQUEST['query'])

    result = [ { m.sattr_prefix : m.to_structure() } for m in qs ]
    return construct_retval(request, result)

## function: delete_vurl
## declared args: vid
def delete_vurl(request, vid, *args, **kwargs):
    """delete_vurl(vid) returns ..."""
    return delete_foo(request, Vurl, vid)

## rest: GET /api/vurl/VID.FMT
## function: read_vurl
## declared args: vid
def read_vurl(request, vid, *args, **kwargs):
    """read_vurl(vid) returns ..."""
    return read_foo(request, Vurl, vid)

## rest: POST /api/vurl/VID.FMT
## function: update_vurl
## declared args: vid
def update_vurl(request, vid, *args, **kwargs):
    """update_vurl(vid) returns ..."""
    return update_foo(request, Vurl, vid)

## function: delete_vurl_key
## declared args: vid sattr
def delete_vurl_key(request, vid, sattr, *args, **kwargs):
    """delete_vurl_key(vid, sattr) returns ..."""
    return delete_foo_key(Vurl, vid, sattr)

## rest: GET /api/vurl/VID/SATTR.FMT
## function: get_vurl_key
## declared args: vid sattr
def get_vurl_key(request, vid, sattr, *args, **kwargs):
    """get_vurl_key(vid, sattr) returns ..."""
    return get_foo_key(Vurl, vid, sattr)

##################################################################
##################################################################
##################################################################
