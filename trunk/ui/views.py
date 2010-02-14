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

from django.shortcuts import render_to_response

from pymine.api.models import Tag, Item, Feed, Comment, Vurl
import pymine.api.views as api

##################################################################

# this definition (create_comment) is auto-generated.
# ensure that any changes are made via the generator.
def create_comment(request, template, idz, **kwargs):
    """
    arguments: request, template, idz, **kwargs
    implements: GET /ui/create/comment/(IDZ).html
    returns: ...
    """
    s = {'itemId': idz}
    return render_to_response(template, s)

##################################################################

# this definition (dash_comments) is auto-generated.
# ensure that any changes are made via the generator.
def dash_comments(request, template, **kwargs):
    """
    arguments: request, template, **kwargs
    implements: GET /ui/dash/comments.html
    returns: ...
    """
    iid = 0
    s = api.list_comments(request, iid)
    s['itemId'] = iid # HACK TO SUPPORT PAGE
    return render_to_response(template, s)

##################################################################

# this definition (dash_things) is auto-generated.
# ensure that any changes are made via the generator.
def dash_things(request, template, thyng, **kwargs):
    """
    arguments: request, template, thyng, **kwargs
    implements: GET /ui/dash/feeds.html
    implements: GET /ui/dash/items.html
    implements: GET /ui/dash/tags.html
    implements: GET /ui/dash/vurls.html
    returns: ...
    """
    s = api.list_things(request, thyng)
    return render_to_response(template, s)

##################################################################

# this definition (delete_thing) is auto-generated.
# ensure that any changes are made via the generator.
def delete_thing(request, template, idname, id, **kwargs):
    """
    arguments: request, template, idname, id, **kwargs
    implements: GET /ui/delete/comment/(ID).html
    implements: GET /ui/delete/feed/(ID).html
    implements: GET /ui/delete/item/(ID).html
    implements: GET /ui/delete/tag/(ID).html
    implements: GET /ui/delete/vurl/(ID).html
    returns: ...
    """
    s = {idname:id}
    return render_to_response(template, s)

##################################################################

# this definition (list_comments) is auto-generated.
# ensure that any changes are made via the generator.
def list_comments(request, template, idz, **kwargs):
    """
    arguments: request, template, idz, **kwargs
    implements: GET /ui/list/comments/(IDZ).html
    returns: ...
    """
    s = api.list_comments(request, iiz)
    s['itemId'] = idz # NEEDED HACK TO SUPPORT PAGE
    return render_to_response(template, s)

##################################################################

# this definition (list_things) is auto-generated.
# ensure that any changes are made via the generator.
def list_things(request, template, thyng, **kwargs):
    """
    arguments: request, template, thyng, **kwargs
    implements: GET /ui/list/feeds.html
    implements: GET /ui/list/items.html
    implements: GET /ui/list/tags.html
    implements: GET /ui/list/vurls.html
    returns: ...
    """
    s = api.list_things(request, Item)
    return render_to_response(template, s)

##################################################################

# this definition (read_thing) is auto-generated.
# ensure that any changes are made via the generator.
def read_thing(request, template, thyng, id, **kwargs):
    """
    arguments: request, template, thyng, id, **kwargs
    implements: GET /ui/read/comment/(ID).html
    implements: GET /ui/read/feed/(ID).html
    implements: GET /ui/read/item/(ID).html
    implements: GET /ui/read/tag/(ID).html
    implements: GET /ui/read/vurl/(ID).html
    returns: ...
    """
    s = api.read_thing(request, thyng, id)
    return render_to_response(template, s)

##################################################################

# this definition (render_page) is auto-generated.
# ensure that any changes are made via the generator.
def render_page(request, template, **kwargs):
    """
    arguments: request, template, **kwargs
    implements: GET /ui/create/feed.html
    implements: GET /ui/create/item.html
    implements: GET /ui/create/tag.html
    implements: GET /ui/create/vurl.html
    implements: GET /ui/dash/home.html
    implements: GET /ui/dash/search.html
    implements: GET /ui/dash/settings.html
    implements: GET /ui/search/comments.html
    implements: GET /ui/search/feeds.html
    implements: GET /ui/search/items.html
    implements: GET /ui/search/tags.html
    implements: GET /ui/search/vurls.html
    returns: ...
    """
    s = {}
    return render_to_response(template, s)

##################################################################

# this definition (update_thing) is auto-generated.
# ensure that any changes are made via the generator.
def update_thing(request, template, thyng, id, **kwargs):
    """
    arguments: request, template, thyng, id, **kwargs
    implements: GET /ui/update/comment/(ID).html
    implements: GET /ui/update/feed/(ID).html
    implements: GET /ui/update/item/(ID).html
    implements: GET /ui/update/tag/(ID).html
    implements: GET /ui/update/vurl/(ID).html
    returns: ...
    """
    s = api.update_thing(request, thyng, id)
    return render_to_response(template, s)

##################################################################

# this definition (version) is auto-generated.
# ensure that any changes are made via the generator.
def version(request, template, **kwargs):
    """
    arguments: request, template, **kwargs
    implements: GET /ui/version.html
    returns: ...
    """
    s = api.read_version()
    return render_to_response(template, s)

##################################################################
