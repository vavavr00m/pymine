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
Work in progress commandline tool/library to upload a Firefox or
Delicious bookmark file as independent Mine items
"""

import re
from beautifulsoup.BeautifulSoup import BeautifulSoup

file = open("test.html", "rb")
doc = file.read()
file.close()

soup = BeautifulSoup(doc)
dl = soup.dl
dl.extract()

for dt in dl.findAll('dt'):
    dd = dt.nextSibling

    title = None
    href = None
    tags = None
    private = False
    description = None

    for a in dt.findAll():
        title = a.string

        href = a['href']
        date = int(a['add_date'])

        if a['private']:
            if int(a['private']):
                private = True

        if a['tags']:
            tags = a['tags']
            tags = [ re.sub(r'\W+', '_', x) for x in tags.split(',') ]
            tags.sort()

    if dd:
        description = dd.string

    print "title>", title
    print "private>", private
    print "href>", href
    print "tags>", tags
    print "date>", date
    print
    print description
    print

