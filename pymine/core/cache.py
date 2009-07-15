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

from UserDict import UserDict

##################################################################

# inspiration
# http://code.sixapart.com/svn/memcached/trunk/server/doc/protocol.txt

class Cache(UserDict):
    """..."""

    def __init__(self, mine):
	"""cache setup"""
	self.mine = mine

    def set(self):
        pass

    def add(self):
        pass

    def replace(self):
        pass

    def get(self):
        pass

    def delete(self):
        pass

    def flush(self):
        pass

    def stats(self):
        pass

