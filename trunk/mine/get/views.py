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

##################################################################

## url: /get
## method: read_minekey
## args: 
def read_minekey(request, *args, **kwargs):
    raise Http404('method read_minekey for url /get is not yet implemented')

## url: /get
## method: create_minekey
## args: 
def create_minekey(request, *args, **kwargs):
    raise Http404('method create_minekey for url /get is not yet implemented')
