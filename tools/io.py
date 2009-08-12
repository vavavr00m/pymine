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

class FileBlockIterator(object):
    """returns an iterator to hack through a (read-binary) File object in blocks, default size 64k"""

    def __init__(self, filename, bsize=(64 * 1024)):
        self._file = open(filename, "rb")
        self._bsize = bsize

    def __getattr__(self, name):
        try: return self.__dict__[name]
        except KeyError: 
            if hasattr(self._file, name): 
                return getattr(self._file, name)
        return None

    def __iter__(self):
        return self

    def next(self):
        b = self._file.read(self._bsize)
        if b == '': raise StopIteration
        return b

import sys

if __name__ == '__main__':
    for block in FileBlockIterator("/etc/services", 64):
        sys.stdout.write(block)
