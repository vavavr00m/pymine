#!/usr/bin/python
##
## Copyright 2009-2010 Adriana Lukas & Alec Muffett
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

"""
frontend for mimetypes module to fix risk of braindeadness
"""

import mimetypes
import os

class lookup:
    __e2t = {
        '.avi': 'video/x-msvideo',
        '.css': 'text/css',
        '.dcr': 'application/x-director',
        '.gif': 'image/gif',
        '.htm': 'text/html',
        '.html': 'text/html',
        '.ico': 'image/vnd.microsoft.icon',
        '.jpeg': 'image/jpeg',
        '.jpg': 'image/jpeg',
        '.js': 'application/javascript',
        '.json': 'application/json',
        '.mov': 'video/quicktime',
        '.pdf': 'application/pdf',
        '.ps': 'application/postscript',
        '.png': 'image/png',
        '.ram': 'audio/x-pn-realaudio',
        '.rm': 'application/vnd.rn-realmedia',
        '.swf': 'application/x-shockwave-flash',
        '.txt': 'text/plain',
        }

    __t2e = {}

    for e, t in __e2t.items():
        __t2e[t] = e

    @staticmethod
    def guess_type(path):
        head, tail = os.path.split(path)
        base, ext = os.path.splitext(tail)
        ext = ext.lower()

        type = lookup.__e2t.get(ext, None)
        enc = None
        if not type:
            type, enc = mimetypes.guess_type(path)
        if not type:
            type = 'application/octet-stream'
            enc = None
        return (type, enc)

    @staticmethod
    def guess_extension(type):
        ext = lookup.__t2e.get(type, None)
        if not ext:
            ext = mimetypes.guess_extension(type)
        if not ext:
            ext = '.dat'
        return ext

if __name__ == '__main__':
    print lookup.guess_type('1.txt')
    print lookup.guess_type('2.ps')
    print lookup.guess_type('3/3.pdf')
    print lookup.guess_type('4/4/4.4.js')

    print lookup.guess_extension('text/plain')
    print lookup.guess_extension('text/html')
    print lookup.guess_extension('application/postscript')
    print lookup.guess_extension('cheese/burger')
