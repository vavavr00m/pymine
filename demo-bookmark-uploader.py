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

from beautifulsoup.BeautifulSoup import BeautifulSoup
import getpass
import miner
import re

url = 'http://localhost:9862'
u = 'pickaxe'
p = getpass.getpass()

# where we store the work in progress
bookmarks = []

# assume an input is in test.html; suck it up
file = open("test.html", "rb")
doc = file.read()
file.close()

# and make soup
soup = BeautifulSoup(doc)

# rip out the definition list
dl = soup.dl

# and actually extract it for tidyness (strictly not needed but it is
# interesting to see what gets left behind
dl.extract()

# hack through the list of DTs and assume that the DD is the sigling
# immediately following
for dt in dl.findAll('dt'):
    dd = dt.nextSibling

    title = None
    link = None
    tags = None
    private = False
    description = None

    for a in dt.findAll():
	link = a['href']
	datestr = a['add_date']

        if a.string:
            title = a.string

	if a['private']:
	    if int(a['private']):
		private = True

	if a['tags']:
	    tags = a['tags']
	    tags = [ re.sub(r'\W+', '_', x) for x in tags.split(',') ]
	    tags.sort()

    if dd and dd.string:
	description = " ".join(dd.string.split())
        description = description

    bookmarks.append(dict(title=title,
			  link=link,
			  tags=tags,
			  private=private,
			  description=description,
			  datestr=datestr))


print "connecting to mine..."
api = miner.MineAPI(username=u, password=p, url_prefix=url)
print

print "print version to check connection..."
print api.version()
print

print "uploading %d bookmarks..." % len(bookmarks)

for bookmark in bookmarks:
    # come up with some boring description template
    d = '<a href="%s" rel="link">%s</a><br/>%s' % (bookmark['link'], bookmark['title'], bookmark['description'])

    iargs = {}

    for s,d in (('title', 'itemName'), 
                ('description', 'itemDescription'),                
                ('link', '$bookmark_url'),
                ('datestr', '$bookmark_date'),
                ):
        if bookmark[s]:
            iargs[d] = bookmark[s].encode('utf-8')

    iargs['itemStatus'] = 'inaccessible' if bookmark['private'] else 'citable'
    iargs['auto_tag'] = 1

    if bookmark['tags']:
        iargs['itemTags'] = " ".join(bookmark['tags']).encode('utf-8')
 
    print "uploading:"
    print iargs

    try:
        item = api.create_item(**iargs)
        if not item:
            print "unexpected null value"
            break
        print '----------'
        print item
        print
        print '=========='
    except Exception, e:
        print e
        print e.read()
        print iargs
        break
