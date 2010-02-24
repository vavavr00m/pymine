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

"""
a minekey is the tuple of data necessary to access items in a mine
"""

from django.http import HttpResponse, HttpResponseForbidden, \
    HttpResponseNotAllowed, HttpResponseNotFound, \
    HttpResponsePermanentRedirect, HttpResponseRedirect

from pymine.api.models import Feed, Item
from pymine.api.feedgen import generate_feed

##################################################################

from views import read_item_data, read_item_icon

import base64
import hashlib
import hmac
import re

import pymine.util.mimestuff as mimestuff

# minekey format:
# hmac/fid/fversion/iid/depth/type.ext
# type in ( data, icon, submit )
# fid in 1..n
# fversion in 1..n
# iid in 1..n
# depth in 3..0
# hmac is base64_web with stripped "="

class MineKey:
    def __init__(self, request, **kwargs):
	"""
	Create a nu-format minekey.

	request: request object for URL-generation purposes

	kwargs include:
	type: one of ('data', 'icon', 'submit')
	fid: integer feed id > 0
	fversion: integer feed version number > 0
	iid: integer item id >= 0
	depth: integer depth > 0
	ext: regexp ^\w+$
	hmac: hmac against which to check this minekey

	if either 'hmac' is supplied, or if kwargs[enforce_hmac_check]
	evaluates to True, a hmac test is performed; this option is
	provided to allow the programmer to ENFORCE a hmac check, just
	in case something higher-up permits code to slide through that
	sets hmac=None/False/0
	"""

	self.__request = request

	self.__depth = int(kwargs.get('depth', -1))
	self.__fid = int(kwargs.get('fid', -1))
	self.__fversion = int(kwargs.get('fversion', -1))
	self.__iid = int(kwargs.get('iid', -1))
	self.__type = kwargs.get('type', None)

	self.__hmac_supplied = kwargs.get('hmac', None)
	self.__ext_supplied = kwargs.get('ext', None)
	self.__item_cached = None
	self.__feed_cached = None

	self.validate()

	enforce_hmac_check = kwargs.get('enforce_hmac_check', False) or self.__hmac_supplied

	if enforce_hmac_check:
	    self.get_hmac(True)

    @classmethod
    def create_feedmk(klass, request, feed):
	"""
	assuming 'feed' is a valid Feed object instance, return a
	minekey which eventually will yield the FEEDXML feed for this
	Feed

	There once was a time when Feed objects were called
	'Relations' because they held data pertinent to the
	relationship between a mine user and one of his subscribers;
	this concept seemed to the programmer to be distinct from
	(say) the feeds that would be generated.

	However this terminology was deemed "confusing" by the Mine
	design team and so now we have Feed objects (one thing) which
	generate feeds (another thing entirely) - obvious, n'est-ce
	pas?
	"""

	return MineKey(request,
		       depth=3,
		       fid=feed.id,
		       fversion=feed.version,
		       iid=0,
		       type='data')

    def __str__(self):
	"""
	returns the minekey information WITHOUT hmac, in the following format:

	fid/fversion/iid/depth/type
	"""
	return "%d/%d/%d/%d/%s" % (
	    self.__fid,
	    self.__fversion,
	    self.__iid,
	    self.__depth,
	    self.__type,
	    )

    def mkerr(self, *args):
	"""create a diag string to drop into an exception"""
	msg = " ".join([ str(x) for x in args ])
	return "MineKey error: %s [%s]" % (msg, str(self))

    def validate(self):
	"""
	does a variety of sanity checks on self and throws a
	RuntimeError if surprised; this does not enforce security
	checks (see access_check()) but instead checks the plausible
	validity of the key itself.

	for a minekey such as "HMAC/42/1/11/2/data.dat" - the
	validation covers everything from "HMAC" to "data" inclusive;
	the trailing ".dat" is considered advisory.
	"""

	if self.__fid <= 0:
	    raise RuntimeError, self.mkerr('fid <= 0')
	if self.__fversion <= 0:
	    raise RuntimeError, self.mkerr('fversion <= 0')
	if self.__iid < 0:
	    raise RuntimeError, self.mkerr('iid < 0')
	if self.__depth not in (3, 2, 1, 0):
	    raise RuntimeError, self.mkerr('depth not in bounds')
	if self.__type not in ('data', 'icon', 'submit'):
	    raise RuntimeError, self.mkerr('type not in permitted set')

    def get_hmac(self, enforce_hmac_check=False):
	"""
	computes and returns the hmac for this minekey

	if enforce_hmac_check evaluates as True (default False) then
	the computed hmac is compared against the hmac declared at
	instantiation; if there is a difference, an exception is
	thrown.
	"""

	hmac_key = '12345678901234567890123456789012'
	hmac_pad = '________________________________'
	h = hmac.new(hmac_key, str(self), hashlib.sha256)
	h.update(hmac_pad)
	hash = base64.urlsafe_b64encode(h.digest()).rstrip('=')

	if enforce_hmac_check:
	    if self.__hmac_supplied != hash:
		raise RuntimeError, self.mkerr('computed hmac "%s" != supplied hmac "%s"' %
					      (hash, self.__hmac_supplied))
	return hash

    def get_feed(self):
	"""return a (cached) copy of the feed object corresponding to this minekey"""
	if not self.__feed_cached:
	    self.__feed_cached = Feed.get(id=self.__fid)
	return self.__feed_cached

    def get_item(self):
	if not self.__item_cached:
	    if self.__iid:
		self.__item_cached = Item.get(id=self.__iid)
	return self.__item_cached

    def get_ext(self):
	"""return a viable extention for this key"""

	if self.__type == 'submit':
	    return '.post'

	elif self.__type == 'data':
	    if self.__iid == 0:
		return ".feed"
	    else:
		i = self.get_item()
		return mimestuff.lookup.guess_extension(i.get_data_type()) or ".dat"

	elif self.__type == 'icon':
	    if self.__iid == 0:
		return ".png"  # TBD: HAVE AN ICON FOR THE USER/MINE OWNER???
	    else:
		i = self.get_item()
		return mimestuff.lookup.guess_extension(i.get_icon_type()) or ".dat"
	else:
	    return ".this-cant-happen"

    def key(self):
	"""
	validates, and then returns the minekey information WITH hmac, in the following format:

	hmac/[fid/fversion/iid/depth/type].ext

	...the [central portion] being generated by __str__() and protected by hmac
	"""

	self.validate()
	hmac = self.get_hmac()
	ext = self.get_ext()

	return "%s/%s%s" % (hmac, str(self), ext)

    def permalink(self):
	"""
	takes the result of self.key() and embeds / returns it in a
	permalink string for this mine; for full pathname resolution
	it needs 'request' to be set in the minekey constructor, or in
	a parent thereof
	"""

	link = "/key/%s" % self.key()

	if self.__request:
	    link = self.__request.build_absolute_uri(link)

	return link

    def http_path(self):
	"""
	returns the http://host.domain:port/ for this mine, for template use
	"""

	link = "/"

	if self.__request:
	    link = self.__request.build_absolute_uri(link)

	return link

    def clone(self):
	"""
	clone this minekey for further futzing

	if you do futz manually, remember to do minekey.validate()
	"""

	foo = {
	    'depth': self.__depth,
	    'fid': self.__fid,
	    'fversion': self.__fversion,
	    'iid': self.__iid,
	    'type': self.__type,
	    }

	return MineKey(self.__request, **foo)

    def spawn_data(self, iid):
	"""
	from this minekey, spawn a new minekey object for the same
	fid/fversion, but for a different iid, decrementing depth
	"""
	if self.__type != 'data':
	    raise RuntimeError, 'cannot spawn another minekey out of non-data minekey: ' + str(self)

	retval = self.clone()
	retval.__iid = iid
	retval.__depth -= 1 # decrement will be checked by validate
	retval.validate() # if we futz with it, we must validate
	return retval

    def spawn_icon(self, iid):
	"""
	from this minekey, spawn a new minekey object for the same
	fid/fversion, but for a different iid's icon, decrementing
	depth
	"""

	if self.__type != 'data':
	    raise RuntimeError, 'cannot spawn a "icon" minekey out of non-data minekey: ' + str(self)

	if self.__depth <= 0:
	    raise RuntimeError, 'cannot spawn a "icon" minekey out of minekey lacking depth: ' + str(self)

	retval = self.clone()
	retval.__type = 'icon'
	retval.__iid = iid
	retval.__depth = 1 # forced to 1, hence check above
	retval.validate() # if we futz with it, we must validate
	return retval

    def spawn_icon_self(self):
	"""
	return spawn_icon for self
	"""
	return self.spawn_icon(self.__iid)

    def spawn_submit(self, iid):
	"""
	from this minekey, spawn a new minekey object for comment
	submission, setting depth=1 if depth is currently legal
	"""

	if self.__type != 'data':
	    raise RuntimeError, 'cannot spawn a "submit" minekey out of non-data minekey: ' + str(self)

	if self.__depth <= 0:
	    raise RuntimeError, 'cannot spawn a "submit" minekey out of minekey lacking depth: ' + str(self)

	retval = self.clone()
	retval.__type = 'submit'
	retval.__iid = iid
	retval.__depth = 1 # forced to 1, hence check above
	retval.validate() # if we futz with it, we must validate
	return retval

    def spawn_submit_self(self):
	"""
	from this minekey, spawn a new minekey object for comment
	submission, setting depth=1 if depth is currently legal
	"""
	return self.spawn_submit(self.__iid)

    def access_check(self):
	"""
	checks the per-feed security policy and enforces it
	"""

	# check ToD against global embargo time

	# check against permitted global IP addresses (WHITELIST/BLACKLIST)

	# check if feed exists / is deleted
	f = self.get_feed()

	# check feed version
	if f.version != self.__fversion:
	    raise RuntimeError, self.mkerr("DB fversion %d not equal to MK fversion %d for %d" %
					   (f.version,
					    self.__fversion,
					    self.__fid))

	# check ToD against feed embargo time

	# check against permitted feed IP addresses (WHITELIST)

	# if DATA&&IID>0 or ICON&&IID>0
	## check if item exists / is deleted
	## check if the item is shared sufficiently enough
	## check if not: restriction applies on Item
	## check if feed has exclude:<Tag> pertinent to the Item

    def response(self):
	"""returns the appropriate http response for this minekey"""
	self.access_check() # abort if the access checks fail

        if self.__type == 'data':
            if self.__iid: # it's an item
                return read_item_data(self.__request, self.__iid, None)
            else: # it's a feed
                return generate_feed(self)
        elif self.__type == 'icon':
                return read_item_icon(self.__request, self.__iid, None)            
        elif self.__type == 'submit':
            pass
        else:
            raise RuntimeError, "this can't happen: " + str(self)


    ##################################################################
    ##################################################################
    ##################################################################

    # THIS NEEDS A REWRITE
    # THIS NEEDS A REWRITE
    # THIS NEEDS A REWRITE

    html_re = re.compile(r"""(SRC|HREF)\s*=\s*(['"]?)/api/(DATA|ICON|SUBMIT)/(\d+)([^\s\>]*)""", re.IGNORECASE)

    def rewrite_html(self, html):
	"""
	using the context of this minekey, rewrite the blob of HTML
	(argument) looking for strings of the form:

	HREF=/api/data/99
	HREF=/api/data/99/dummy.html
	HREF='/api/data/99/dummy.html'
	HREF="/api/data/99"
	SRC=/api/icon/99/dummy.png
	SRC='/api/icon/99'
	SRC="/api/icon/99/dummy.png"

	...where 99 is an example iid; the rewriter replacing the 99
	with the results of self.spawn_data(iid).permalink() - in other
	words a URL customised to retreive that item/iid with
	decremented depth.

	The rewriter tries to be semi-clever, but not very, alas; it
	does not check that we are currently inside a <TAG> before
	rewriting such strings.  When BeautifulSoup comes in, that
	will change.

	if the /api/icon/99/dummy.png URL is prefixed with either a
	single or double-quote, the rewriter checks that the substring
	to be rewritten ends with a corresponding quote; this is
	inadequate but should hope with unbalanced quotation marks
	during development.

	if the URL does NOT begin with a quote character, the rewriter
	ignores what the last character of the matched string,
	irrespective of whether it is a quote character or not.

	if any sanity-check fails, the rewriter simply does not
	rewrite the HTML.
	"""

	def rewrite_link(mo):
	    """backend link rewriter for code clarity"""
	    action = mo.group(1)
	    quote = mo.group(2)
	    what = mo.group(3)
	    iid = int(mo.group(4))
	    suffix = mo.group(5)

	    if quote and (not suffix.endswith(quote)):
		return mo.group(0)

	    if what == 'data':
		rewrite = self.spawn_data(iid).permalink()
	    elif what == 'icon':
		rewrite = self.spawn_icon(iid).permalink()
	    elif what == 'submit':
		rewrite = self.spawn_submit(iid).permalink()
	    else:
		return mo.group(0)

	    return '%s="%s"' % (action, rewrite)

	return self.html_re.sub(rewrite_link, html)

##################################################################

if __name__ == '__main__':
    foo = {
	'type': 'data',
	'fid': 2,
	'fversion': 1,
	'iid': 0,
	'depth': 3,
	}

    mk = MineKey(None, **foo)
    print "1a", mk
    print "1b", mk.key()
    print "1c", mk.permalink()

    x = mk.spawn_submit_self()
    print "2", x.key()

    y = mk.spawn_data(4)
    print "3", y.key()

    print "4", y.spawn_submit_self().key()

    print "5a", mk.rewrite_html('--<A HREF=/api/data/1.jpg/foo>foo</A>--')
    print "5b", mk.rewrite_html('--<A HREF=/api/data/1.jpg/foo>foo</A>--')
    print "5c", mk.rewrite_html('--<A HREF=/api/data/1..../foo>foo</A>--')
    print "5d", mk.rewrite_html('--<A HREF=/api/data/1..../foo>foo</A>--')
    print "5e", mk.rewrite_html('--<A HREF=/api/data/1..../foo>foo</A>--')
    print "5f", mk.rewrite_html('--<A HREF=/api/data/1..../foo>foo</A>--')

    print "7a", mk.rewrite_html('--<A HREF="/api/data/1">foo</A>--')
    print "7b", mk.rewrite_html('--<A HREF="/api/data/1.pdf">foo</A>--')
    print "7c", mk.rewrite_html('--<A HREF="/api/data/1.jpg">foo</A>--')

    print "8", mk.rewrite_html('--<A HREF="/api/icon/2">foo</A>--')

    print "9", mk.rewrite_html('--<A HREF="/api/submit/3">foo</A>--')

    print "10a", mk.rewrite_html('--<A HREF="/api/data/0">foo</A>--')
    print "10b", mk.rewrite_html('--<A HREF="/api/icon/0">foo</A>--')
    print "10c", mk.rewrite_html('--<A HREF="/api/submit/0">foo</A>--')

