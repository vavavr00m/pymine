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
from pymine.views import HTTP_AUTH
import views as dev

urlpatterns = patterns('',
		       )

##################################################################
# this code is auto-generated.
# ensure that any changes are made via the generator.

urlpatterns += patterns('',
			(r'^home\.html$',
			 HTTP_AUTH, { 'GET' : [ dev.render, 'dev/tbd.html' ], }),
			)

##################################################################
