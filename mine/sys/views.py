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

## rest: GET /sys
## function: read_sys_root
## declared args: 
def read_sys_root(request, *args, **kwargs):
    return render_to_response('read-sys-root.html')

## rest: GET /sys/export
## function: sys_export
## declared args: 
def sys_export(request, *args, **kwargs):
    return render_to_response('sys-export.html')

## rest: GET /sys/import
## function: sys_import
## declared args: 
def sys_import(request, *args, **kwargs):
    return render_to_response('sys-import.html')

## rest: GET /sys/cleanup
## function: sys_cleanup
## declared args: 
def sys_cleanup(request, *args, **kwargs):
    return render_to_response('sys-cleanup.html')

