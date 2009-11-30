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

"""docstring goes here""" # :-)

import base64

b64_alt = '-_'

def encode(value):
    """b64encode using the mine standard escape characters"""
    return base64.b64encode(value, b64_alt)

def decode(encoded):
    """b64decode using the mine standard escape characters"""
    return base64.b64decode(encoded.encode('utf-8'), b64_alt)
