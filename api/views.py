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

from envelope import Envelope

##################################################################

# this definition (create_comment) is auto-generated.
# ensure that any changes are made via the generator.
def create_comment(request, idz, **kwargs):
    """
    arguments: request, idz, **kwargs
    implements: POST /api/comment/item/(IDZ).(FMT)
    returns: ...
    """
    s = {}
    return Envelope(request, s)

##################################################################

# this definition (create_thing) is auto-generated.
# ensure that any changes are made via the generator.
def create_thing(request, thyng, **kwargs):
    """
    arguments: request, thyng, **kwargs
    implements: POST /api/feed.(FMT)
    implements: POST /api/item.(FMT)
    implements: POST /api/tag.(FMT)
    implements: POST /api/vurl.(FMT)
    returns: ...
    """
    s = {}
    return Envelope(request, s)

##################################################################

# this definition (delete_registry_attr) is auto-generated.
# ensure that any changes are made via the generator.
def delete_registry_attr(request, rattr, **kwargs):
    """
    arguments: request, rattr, **kwargs
    implements: DELETE /api/registry/(RATTR).(FMT)
    returns: ...
    """
    s = {}
    return Envelope(request, s)

##################################################################

# this definition (delete_thing) is auto-generated.
# ensure that any changes are made via the generator.
def delete_thing(request, thyng, id, **kwargs):
    """
    arguments: request, thyng, id, **kwargs
    implements: DELETE /api/comment/(ID).(FMT)
    implements: DELETE /api/feed/(ID).(FMT)
    implements: DELETE /api/item/(ID).(FMT)
    implements: DELETE /api/tag/(ID).(FMT)
    implements: DELETE /api/vurl/(ID).(FMT)
    returns: ...
    """
    s = {}
    return Envelope(request, s)

##################################################################

# this definition (delete_thing_attr) is auto-generated.
# ensure that any changes are made via the generator.
def delete_thing_attr(request, thyng, id, attr, **kwargs):
    """
    arguments: request, thyng, id, attr, **kwargs
    implements: DELETE /api/comment/(ID)/(ATTR).(FMT)
    implements: DELETE /api/feed/(ID)/(ATTR).(FMT)
    implements: DELETE /api/item/(ID)/(ATTR).(FMT)
    implements: DELETE /api/tag/(ID)/(ATTR).(FMT)
    implements: DELETE /api/vurl/(ID)/(ATTR).(FMT)
    returns: ...
    """
    s = {}
    return Envelope(request, s)

##################################################################

# this definition (encode_minekey) is auto-generated.
# ensure that any changes are made via the generator.
def encode_minekey(request, **kwargs):
    """
    arguments: request, **kwargs
    implements: POST /api/encode.(FMT)
    returns: ...
    """
    s = {}
    return Envelope(request, s)

##################################################################

# this definition (get_registry_attr) is auto-generated.
# ensure that any changes are made via the generator.
def get_registry_attr(request, rattr, **kwargs):
    """
    arguments: request, rattr, **kwargs
    implements: GET /api/registry/(RATTR).(FMT)
    returns: ...
    """
    s = {}
    return Envelope(request, s)

##################################################################

# this definition (get_thing_attr) is auto-generated.
# ensure that any changes are made via the generator.
def get_thing_attr(request, thyng, id, attr, **kwargs):
    """
    arguments: request, thyng, id, attr, **kwargs
    implements: GET /api/comment/(ID)/(ATTR).(FMT)
    implements: GET /api/feed/(ID)/(ATTR).(FMT)
    implements: GET /api/item/(ID)/(ATTR).(FMT)
    implements: GET /api/tag/(ID)/(ATTR).(FMT)
    implements: GET /api/vurl/(ID)/(ATTR).(FMT)
    returns: ...
    """
    s = {}
    return Envelope(request, s)

##################################################################

# this definition (list_comments) is auto-generated.
# ensure that any changes are made via the generator.
def list_comments(request, idz, **kwargs):
    """
    arguments: request, idz, **kwargs
    implements: GET /api/comment/item/(IDZ).(FMT)
    returns: ...
    """
    s = {}
    return Envelope(request, s)

##################################################################

# this definition (list_registry) is auto-generated.
# ensure that any changes are made via the generator.
def list_registry(request, **kwargs):
    """
    arguments: request, **kwargs
    implements: GET /api/registry.(FMT)
    returns: ...
    """
    s = {}
    return Envelope(request, s)

##################################################################

# this definition (list_things) is auto-generated.
# ensure that any changes are made via the generator.
def list_things(request, thyng, **kwargs):
    """
    arguments: request, thyng, **kwargs
    implements: GET /api/feed.(FMT)
    implements: GET /api/item.(FMT)
    implements: GET /api/tag.(FMT)
    implements: GET /api/vurl.(FMT)
    returns: ...
    """
    s = {}
    return Envelope(request, s)

##################################################################

# this definition (query_thing) is auto-generated.
# ensure that any changes are made via the generator.
def query_thing(request, thyng, **kwargs):
    """
    arguments: request, thyng, **kwargs
    implements: GET /api/query/comment.(FMT)
    implements: GET /api/query/feed.(FMT)
    implements: GET /api/query/item.(FMT)
    implements: GET /api/query/tag.(FMT)
    implements: GET /api/query/vurl.(FMT)
    returns: ...
    """
    s = {}
    return Envelope(request, s)

##################################################################

# this definition (read_item_data) is auto-generated.
# ensure that any changes are made via the generator.
def read_item_data(request, id, token, **kwargs):
    """
    arguments: request, id, token, **kwargs
    implements: GET /api/data/(ID)(/TOKEN)
    returns: ...
    """
    s = {}
    return Envelope(request, s)

##################################################################

# this definition (read_item_icon) is auto-generated.
# ensure that any changes are made via the generator.
def read_item_icon(request, id, token, **kwargs):
    """
    arguments: request, id, token, **kwargs
    implements: GET /api/icon/(ID)(/TOKEN)
    returns: ...
    """
    s = {}
    return Envelope(request, s)

##################################################################

# this definition (read_thing) is auto-generated.
# ensure that any changes are made via the generator.
def read_thing(request, thyng, id, **kwargs):
    """
    arguments: request, thyng, id, **kwargs
    implements: GET /api/comment/(ID).(FMT)
    implements: GET /api/feed/(ID).(FMT)
    implements: GET /api/item/(ID).(FMT)
    implements: GET /api/tag/(ID).(FMT)
    implements: GET /api/vurl/(ID).(FMT)
    returns: ...
    """
    s = {}
    return Envelope(request, s)

##################################################################

# this definition (read_version) is auto-generated.
# ensure that any changes are made via the generator.
def read_version(request, **kwargs):
    """
    arguments: request, **kwargs
    implements: GET /api/version.(FMT)
    returns: ...
    """
    s = {}
    return Envelope(request, s)

##################################################################

# this definition (update_registry_attr) is auto-generated.
# ensure that any changes are made via the generator.
def update_registry_attr(request, rattr, **kwargs):
    """
    arguments: request, rattr, **kwargs
    implements: POST /api/registry/(RATTR).(FMT)
    returns: ...
    """
    s = {}
    return Envelope(request, s)

##################################################################

# this definition (update_thing) is auto-generated.
# ensure that any changes are made via the generator.
def update_thing(request, thyng, id, **kwargs):
    """
    arguments: request, thyng, id, **kwargs
    implements: POST /api/comment/(ID).(FMT)
    implements: POST /api/feed/(ID).(FMT)
    implements: POST /api/item/(ID).(FMT)
    implements: POST /api/tag/(ID).(FMT)
    implements: POST /api/vurl/(ID).(FMT)
    returns: ...
    """
    s = {}
    return Envelope(request, s)

##################################################################
