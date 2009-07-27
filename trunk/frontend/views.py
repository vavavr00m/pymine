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

import datetime

def root(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)

def rest(request, *args, **kwargs):
    get_view = kwargs.pop('GET', None)
    post_view = kwargs.pop('POST', None)
    put_view = kwargs.pop('PUT', None)
    delete_view = kwargs.pop('DELETE', None)

    if request.method == 'GET' and get_view is not None:
        return get_view(request, *args, **kwargs)
    elif request.method == 'POST' and post_view is not None:
        return post_view(request, *args, **kwargs)
    elif request.method == 'PUT' and put_view is not None:
        return put_view(request, *args, **kwargs)
    elif request.method == 'DELETE' and delete_view is not None:
        return delete_view(request, *args, **kwargs)

    raise Http404

#------------------------------------------------------------------
#### method: read_config url: api/config.FMT
def read_config(request, *args, **kwargs):
    raise Http404('method read_config for url api/config.FMT is not yet implemented')

#### method: create_config url: api/config.FMT
def create_config(request, *args, **kwargs):
    raise Http404('method create_config for url api/config.FMT is not yet implemented')

#### method: read_item_list url: api/item.FMT
def read_item_list(request, *args, **kwargs):
    raise Http404('method read_item_list for url api/item.FMT is not yet implemented')

#### method: create_item url: api/item.FMT
def create_item(request, *args, **kwargs):
    raise Http404('method create_item for url api/item.FMT is not yet implemented')

#### method: read_item_data url: api/item/IID
def read_item_data(request, iid, *args, **kwargs):
    raise Http404('method read_item_data for url api/item/IID is not yet implemented')

#### method: update_item_data url: api/item/IID
def update_item_data(request, iid, *args, **kwargs):
    raise Http404('method update_item_data for url api/item/IID is not yet implemented')

#### method: delete_item url: api/item/IID.FMT
def delete_item(request, iid, *args, **kwargs):
    raise Http404('method delete_item for url api/item/IID.FMT is not yet implemented')

#### method: read_item url: api/item/IID.FMT
def read_item(request, iid, *args, **kwargs):
    raise Http404('method read_item for url api/item/IID.FMT is not yet implemented')

#### method: delete_comment url: api/item/IID/CID.FMT
def delete_comment(request, iid, cid, *args, **kwargs):
    raise Http404('method delete_comment for url api/item/IID/CID.FMT is not yet implemented')

#### method: read_comment url: api/item/IID/CID.FMT
def read_comment(request, iid, cid, *args, **kwargs):
    raise Http404('method read_comment for url api/item/IID/CID.FMT is not yet implemented')

#### method: create_comment_key url: api/item/IID/CID/key.FMT
def create_comment_key(request, iid, cid, *args, **kwargs):
    raise Http404('method create_comment_key for url api/item/IID/CID/key.FMT is not yet implemented')

#### method: delete_comment_key url: api/item/IID/CID/key/KEY.FMT
def delete_comment_key(request, iid, cid, key, *args, **kwargs):
    raise Http404('method delete_comment_key for url api/item/IID/CID/key/KEY.FMT is not yet implemented')

#### method: read_comment_key url: api/item/IID/CID/key/KEY.FMT
def read_comment_key(request, iid, cid, key, *args, **kwargs):
    raise Http404('method read_comment_key for url api/item/IID/CID/key/KEY.FMT is not yet implemented')

#### method: update_comment_key url: api/item/IID/CID/key/KEY.FMT
def update_comment_key(request, iid, cid, key, *args, **kwargs):
    raise Http404('method update_comment_key for url api/item/IID/CID/key/KEY.FMT is not yet implemented')

#### method: read_clone_list url: api/item/IID/clone.FMT
def read_clone_list(request, iid, *args, **kwargs):
    raise Http404('method read_clone_list for url api/item/IID/clone.FMT is not yet implemented')

#### method: create_clone url: api/item/IID/clone.FMT
def create_clone(request, iid, *args, **kwargs):
    raise Http404('method create_clone for url api/item/IID/clone.FMT is not yet implemented')

#### method: read_comment_list url: api/item/IID/comment.FMT
def read_comment_list(request, iid, *args, **kwargs):
    raise Http404('method read_comment_list for url api/item/IID/comment.FMT is not yet implemented')

#### method: create_comment url: api/item/IID/comment.FMT
def create_comment(request, iid, *args, **kwargs):
    raise Http404('method create_comment for url api/item/IID/comment.FMT is not yet implemented')

#### method: create_item_key url: api/item/IID/key.FMT
def create_item_key(request, iid, *args, **kwargs):
    raise Http404('method create_item_key for url api/item/IID/key.FMT is not yet implemented')

#### method: delete_item_key url: api/item/IID/key/KEY.FMT
def delete_item_key(request, iid, key, *args, **kwargs):
    raise Http404('method delete_item_key for url api/item/IID/key/KEY.FMT is not yet implemented')

#### method: read_item_key url: api/item/IID/key/KEY.FMT
def read_item_key(request, iid, key, *args, **kwargs):
    raise Http404('method read_item_key for url api/item/IID/key/KEY.FMT is not yet implemented')

#### method: update_item_key url: api/item/IID/key/KEY.FMT
def update_item_key(request, iid, key, *args, **kwargs):
    raise Http404('method update_item_key for url api/item/IID/key/KEY.FMT is not yet implemented')

#### method: read_relation_list url: api/relation.FMT
def read_relation_list(request, *args, **kwargs):
    raise Http404('method read_relation_list for url api/relation.FMT is not yet implemented')

#### method: create_relation url: api/relation.FMT
def create_relation(request, *args, **kwargs):
    raise Http404('method create_relation for url api/relation.FMT is not yet implemented')

#### method: delete_relation url: api/relation/RID.FMT
def delete_relation(request, rid, *args, **kwargs):
    raise Http404('method delete_relation for url api/relation/RID.FMT is not yet implemented')

#### method: read_relation url: api/relation/RID.FMT
def read_relation(request, rid, *args, **kwargs):
    raise Http404('method read_relation for url api/relation/RID.FMT is not yet implemented')

#### method: create_relation_key url: api/relation/RID/key.FMT
def create_relation_key(request, rid, *args, **kwargs):
    raise Http404('method create_relation_key for url api/relation/RID/key.FMT is not yet implemented')

#### method: delete_relation_key url: api/relation/RID/key/KEY.FMT
def delete_relation_key(request, rid, key, *args, **kwargs):
    raise Http404('method delete_relation_key for url api/relation/RID/key/KEY.FMT is not yet implemented')

#### method: read_relation_key url: api/relation/RID/key/KEY.FMT
def read_relation_key(request, rid, key, *args, **kwargs):
    raise Http404('method read_relation_key for url api/relation/RID/key/KEY.FMT is not yet implemented')

#### method: update_relation_key url: api/relation/RID/key/KEY.FMT
def update_relation_key(request, rid, key, *args, **kwargs):
    raise Http404('method update_relation_key for url api/relation/RID/key/KEY.FMT is not yet implemented')

#### method: read_tag_list url: api/tag.FMT
def read_tag_list(request, *args, **kwargs):
    raise Http404('method read_tag_list for url api/tag.FMT is not yet implemented')

#### method: create_tag url: api/tag.FMT
def create_tag(request, *args, **kwargs):
    raise Http404('method create_tag for url api/tag.FMT is not yet implemented')

#### method: delete_tag url: api/tag/TID.FMT
def delete_tag(request, tid, *args, **kwargs):
    raise Http404('method delete_tag for url api/tag/TID.FMT is not yet implemented')

#### method: read_tag url: api/tag/TID.FMT
def read_tag(request, tid, *args, **kwargs):
    raise Http404('method read_tag for url api/tag/TID.FMT is not yet implemented')

#### method: create_tag_key url: api/tag/TID/key.FMT
def create_tag_key(request, tid, *args, **kwargs):
    raise Http404('method create_tag_key for url api/tag/TID/key.FMT is not yet implemented')

#### method: delete_tag_key url: api/tag/TID/key/KEY.FMT
def delete_tag_key(request, tid, key, *args, **kwargs):
    raise Http404('method delete_tag_key for url api/tag/TID/key/KEY.FMT is not yet implemented')

#### method: read_tag_key url: api/tag/TID/key/KEY.FMT
def read_tag_key(request, tid, key, *args, **kwargs):
    raise Http404('method read_tag_key for url api/tag/TID/key/KEY.FMT is not yet implemented')

#### method: update_tag_key url: api/tag/TID/key/KEY.FMT
def update_tag_key(request, tid, key, *args, **kwargs):
    raise Http404('method update_tag_key for url api/tag/TID/key/KEY.FMT is not yet implemented')

#### method: read_version url: api/version.FMT
def read_version(request, *args, **kwargs):
    return HttpResponse("hello world, from pymine\n")


#------------------------------------------------------------------
