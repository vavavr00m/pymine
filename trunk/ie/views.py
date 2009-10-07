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

from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404

##################################################################

## rest: GET /ie
## function: root_ie
## declared args: 
def root_ie(request, *args, **kwargs):
    s = api.root_ie(request, *args, **kwargs)
    return render_to_response('root-ie.html', s)

## rest: GET /ie/export
## function: ie_export
## declared args: 
def ie_export(request, *args, **kwargs):
    s = api.ie_export(request, *args, **kwargs)
    return render_to_response('ie-export.html', s)

## rest: GET /ie/import
## function: ie_import
## declared args: 
def ie_import(request, *args, **kwargs):
    s = api.ie_import(request, *args, **kwargs)
    return render_to_response('ie-import.html', s)

