#!/usr/bin/env python
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

from django.conf import settings

class Envelope(dict):
    """
    wrapper-class atop 'dict' to provide a few extra methods
    """

    def __init__(self, request, **kwargs):

	self.update(kwargs)

	if settings.DEBUG:
	    self['__mine_debug_enabled__'] = 1

	    # cascade a few more checks in here
	    if settings.TEMPLATE_STRING_IF_INVALID:
		self['__mine_debug_empty_string__'] = settings.TEMPLATE_STRING_IF_INVALID
