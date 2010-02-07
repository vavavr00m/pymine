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

from django.conf.urls.defaults import *
from pymine.views import API_REST, HTTP_METHOD
import views as api

urlpatterns = patterns('',
		       ##################################################################
		       ##################################################################
		       ##################################################################
		       (r'^comment/(?P<id>[1-9]\d*)/(?P<sattr>\$?[_A-Za-z]\w*)\.(?P<fmt>(json|xml|txt|rdr))$',
			API_REST, { 'DELETE' : [ api.delete_thing_attr, Comment ],
				    'GET' : [ api.get_thing_attr, Comment ],
				    }),
		       (r'^comment/(?P<id>[1-9]\d*)\.(?P<fmt>(json|xml|txt|rdr))$',
			API_REST, { 'DELETE' : [ api.delete_thing, Comment ],
				    'GET' : [ api.read_thing, Comment ],
				    'POST' : [ api.update_thing, Comment ],
				    }),
		       (r'^comment/item/(?P<idz>\d+)\.(?P<fmt>(json|xml|txt|rdr))$',
			API_REST, { 'GET' : [ api.list_comments ],
				    'POST' : [ api.create_comment ],
				    }),
		       (r'^data/(?P<id>[1-9]\d*)(/?P<token>[\-\.\w]*)$',
			HTTP_METHOD, { 'GET' : [ api.read_item_data ],
				       }),
		       (r'^encode\.(?P<fmt>(json|xml|txt|rdr))$',
			API_REST, { 'POST' : [ api.encode_minekey ],
				    }),
		       (r'^feed/(?P<id>[1-9]\d*)/(?P<sattr>\$?[_A-Za-z]\w*)\.(?P<fmt>(json|xml|txt|rdr))$',
			API_REST, { 'DELETE' : [ api.delete_thing_attr, Feed ],
				    'GET' : [ api.get_thing_attr, Feed ],
				    }),
		       (r'^feed/(?P<id>[1-9]\d*)\.(?P<fmt>(json|xml|txt|rdr))$',
			API_REST, { 'DELETE' : [ api.delete_thing, Feed ],
				    'GET' : [ api.read_thing, Feed ],
				    'POST' : [ api.update_thing, Feed ],
				    }),
		       (r'^feed\.(?P<fmt>(json|xml|txt|rdr))$',
			API_REST, { 'GET' : [ api.list_things, Feed ],
				    'POST' : [ api.create_thing, Feed ],
				    }),
		       (r'^icon/(?P<id>[1-9]\d*)(/?P<token>[\-\.\w]*)$',
			HTTP_METHOD, { 'GET' : [ api.read_item_icon ],
				       }),
		       (r'^item/(?P<id>[1-9]\d*)/(?P<sattr>\$?[_A-Za-z]\w*)\.(?P<fmt>(json|xml|txt|rdr))$',
			API_REST, { 'DELETE' : [ api.delete_thing_attr, Item ],
				    'GET' : [ api.get_thing_attr, Item ],
				    }),
		       (r'^item/(?P<id>[1-9]\d*)\.(?P<fmt>(json|xml|txt|rdr))$',
			API_REST, { 'DELETE' : [ api.delete_thing, Item ],
				    'GET' : [ api.read_thing, Item ],
				    'POST' : [ api.update_thing, Item ],
				    }),
		       (r'^item\.(?P<fmt>(json|xml|txt|rdr))$',
			API_REST, { 'GET' : [ api.list_things, Item ],
				    'POST' : [ api.create_thing, Item ],
				    }),
		       (r'^query/comment\.(?P<fmt>(json|xml|txt|rdr))$',
			API_REST, { 'GET' : [ api.query_thing, Comment ],
				    }),
		       (r'^query/feed\.(?P<fmt>(json|xml|txt|rdr))$',
			API_REST, { 'GET' : [ api.query_thing, Feed ],
				    }),
		       (r'^query/item\.(?P<fmt>(json|xml|txt|rdr))$',
			API_REST, { 'GET' : [ api.query_thing, Item ],
				    }),
		       (r'^query/tag\.(?P<fmt>(json|xml|txt|rdr))$',
			API_REST, { 'GET' : [ api.query_thing, Tag ],
				    }),
		       (r'^query/vurl\.(?P<fmt>(json|xml|txt|rdr))$',
			API_REST, { 'GET' : [ api.query_thing, Vurl ],
				    }),
		       (r'^registry/(?P<rattr>[_A-Za-z]\w*)\.(?P<fmt>(json|xml|txt|rdr))$',
			API_REST, { 'DELETE' : [ api.delete_registry_attr ],
				    'GET' : [ api.get_registry_attr ],
				    'POST' : [ api.update_registry_attr ],
				    }),
		       (r'^registry\.(?P<fmt>(json|xml|txt|rdr))$',
			API_REST, { 'GET' : [ api.list_registry ],
				    }),
		       (r'^tag/(?P<id>[1-9]\d*)/(?P<sattr>\$?[_A-Za-z]\w*)\.(?P<fmt>(json|xml|txt|rdr))$',
			API_REST, { 'DELETE' : [ api.delete_thing_attr, Tag ],
				    'GET' : [ api.get_thing_attr, Tag ],
				    }),
		       (r'^tag/(?P<id>[1-9]\d*)\.(?P<fmt>(json|xml|txt|rdr))$',
			API_REST, { 'DELETE' : [ api.delete_thing, Tag ],
				    'GET' : [ api.read_thing, Tag ],
				    'POST' : [ api.update_thing, Tag ],
				    }),
		       (r'^tag\.(?P<fmt>(json|xml|txt|rdr))$',
			API_REST, { 'GET' : [ api.list_things, Tag ],
				    'POST' : [ api.create_thing, Tag ],
				    }),
		       (r'^version\.(?P<fmt>(json|xml|txt|rdr))$',
			API_REST, { 'GET' : [ api.read_version ],
				    }),
		       (r'^vurl/(?P<id>[1-9]\d*)/(?P<sattr>\$?[_A-Za-z]\w*)\.(?P<fmt>(json|xml|txt|rdr))$',
			API_REST, { 'DELETE' : [ api.delete_thing_attr, Vurl ],
				    'GET' : [ api.get_thing_attr, Vurl ],
				    }),
		       (r'^vurl/(?P<id>[1-9]\d*)\.(?P<fmt>(json|xml|txt|rdr))$',
			API_REST, { 'DELETE' : [ api.delete_thing, Vurl ],
				    'GET' : [ api.read_thing, Vurl ],
				    'POST' : [ api.update_thing, Vurl ],
				    }),
		       (r'^vurl\.(?P<fmt>(json|xml|txt|rdr))$',
			API_REST, { 'GET' : [ api.list_things, Vurl ],
				    'POST' : [ api.create_thing, Vurl ],
				    }),
		       ##################################################################
		       ##################################################################
		       ##################################################################
		       )
