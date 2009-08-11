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

## rest: GET /get
## function: read_get_root
## declared args: 
def read_get_root(request, *args, **kwargs):
    raise Http404('backend read_get_root for GET /get is not yet implemented') # TO BE DONE
    return render_to_response('read-get-root.html')

## rest: GET /get/KEY
## function: read_minekey
## declared args: key
def read_minekey(request, key, *args, **kwargs):
    raise Http404('backend read_minekey for GET /get/KEY is not yet implemented') # TO BE DONE
    return render_to_response('read-minekey.html')

## rest: POST /get/KEY
## function: submit_minekey
## declared args: key
def submit_minekey(request, key, *args, **kwargs):
    raise Http404('backend submit_minekey for POST /get/KEY is not yet implemented') # TO BE DONE
    return render_to_response('submit-minekey.html')

