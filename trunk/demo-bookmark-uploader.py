#!/usr/bin/env python
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
import sys

##################################################################

def parse_bookmarks(filename):
    bookmarks = []
    feeds = {}

    fd = open(filename, "rb")
    doc = fd.read()
    fd.close()

    soup = BeautifulSoup(doc)

    # rip out the definition list

    dl = soup.dl

    # extract it for tidyness (strictly not needed but it is
    # interesting to see what gets left behind

    dl.extract()

    # hack through the list of DTs and assume that the DD is the
    # sibling immediately following

    for dt in dl.findAll('dt'):
	dd = dt.nextSibling

	title = None
	link = None
	tags = None
	private = False
	description = None

	for a in dt.findAll(): # should only be one
	    link = a['href']
	    datestr = a['add_date']

	    if a.string:
		title = a.string

	    if a['private']:
		if int(a['private']):
		    private = True

	    if a['tags']:
		tags = []
		for tag in a['tags'].split(','):
		    if tag.startswith('for:') or tag.startswith('not:'):
                        feed = re.sub(r'\W+', '_', tag[4:]).lower()
                        feeds[feed] = feeds.get(feed, 0) + 1
			tags.append(tag)
		    else:
			tags.append(re.sub(r'\W+', '_', tag).lower())
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

    return bookmarks, feeds

##################################################################

def upload_bookmarks(mine, bookmarks):
    print "uploading %d bookmarks..." % len(bookmarks)

    for bookmark in bookmarks:
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

	print "uploading:", iargs

	try:
	    item = mine.create_item(**iargs)
	    if not item:
		print "unexpected null value"
		break
	except Exception, e:
	    print iargs
	    print e
	    print e.read()
	    break

##################################################################

if __name__ == '__main__':
    bookmarks = []

    for filename in sys.argv[1:]:
        bms, feeds = parse_bookmarks(filename)
        bookmarks.extend(bms)
        print "items:", filename, len(bms)
        print "feeds:", filename, feeds

    u = 'pickaxe'
    p = getpass.getpass()
    url = 'http://localhost:9862'

    print "connecting to mine %s as %s" % (u, p)
    mine = miner.MineAPI(username=u, password=p, url_prefix=url)

    print "printing version to check connection..."
    print mine.version()

    print "uploading..."
    print mine.version()

