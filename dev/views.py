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

from django.shortcuts import render_to_response

##################################################################

# this definition (render) is auto-generated.
# ensure that any changes are made via the generator.
def render(request, template, **kwargs):
    """
    arguments: request, template, **kwargs
    implements: GET /dev/home.html
    returns: ...
    """
    s = {}
    return render_to_response(template, s)

##################################################################
