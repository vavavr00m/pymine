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

import base64
import hashlib
import hmac
import re

import util.mimestuff as mimestuff


# minekey format:
# hmac/fid/fversion/iid/depth/type.ext
# type in ( data, icon, submit )
# fid in 1..n
# fversion in 1..n
# iid in 1..n
# depth in 3..0
# hmac is base64_web with stripped "="

class MineKey:
    def __init__(self, **kwargs):
	"""
	Create a nu-format minekey.

	kwargs include:
	type: one of ('data', 'icon', 'submit')
	fid: integer feed id > 0
	fversion: integer feed version number > 0
	iid: integer item id >= 0
	depth: integer depth > 0
	ext: regexp ^\w+$
	hmac: hmac against which to check this minekey
	request: request object for URL-generation purposes
	"""

	self.__depth = kwargs.get('depth', -1)
	self.__fid = kwargs.get('fid', -1)
	self.__fversion = kwargs.get('fversion', -1)
	self.__iid = kwargs.get('iid', -1)
	self.__type = kwargs.get('type', None)

	self.__request = kwargs.get('request', None)
	self.__hmac_supplied = kwargs.get('hmac', None)
	self.__item_cached = None
	self.__feed_cached = None

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

    def validate(self):
	"""
	does a variety of sanity checks on self and throws a RuntimeError if surprised

        returns the stripped hmac string

        for a minekey such as "HASH/42/1/11/2/data.dat" - the
        validation covers everything from "HASH" to "data" inclusive;
        the trailing ".dat" is considered advisory.
	"""

	def errmsg(x):
	    """ """
	    return "MineKey fails validation: %s [%s]" % (x, str(self))

	if self.__fid <= 0:
	    raise RuntimeError, errmsg('fid <= 0')
	if self.__fversion <= 0:
	    raise RuntimeError, errmsg('fversion <= 0')
	if self.__iid < 0:
	    raise RuntimeError, errmsg('iid < 0')
	if self.__depth not in (3, 2, 1, 0):
	    raise RuntimeError, errmsg('depth not in bounds')
	if self.__type not in ('data', 'icon', 'submit'):
	    raise RuntimeError, errmsg('type not in permitted set')

        f = self.get_feed()

        if f.version != self.__fversion:
            raise RuntimeError, errmsg("database feed version %d not equal to minekey feed version %d" % (f.version, self.__fversion))

	hmac_key = '12345678901234567890123456789012'
	hmac_pad = '________________________________'
	h = hmac.new(hmac_key, str(self), hashlib.sha256)
	h.update(hmac_pad)
	hash = base64.urlsafe_b64encode(h.digest()).rstrip('=')

	if self.__hmac_supplied:
	    if self.__hmac_supplied != hash:
		raise RuntimeError, errmsg('computed hmac "%s" does not match supplied hmac "%s"' %
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

    def key(self):
	"""
	validates, and then returns the minekey information WITH hmac, in the following format:

	hmac/fid/fversion/iid/depth/type.ext

	...the central portion being generated by __str__()
	"""

	hash = self.validate()

        if self.__iid == 0:
            ext = 'feed'
        else:
            i = self.get_item() # if None, something is wrong so let it barf

            if self.__type == 'data':
                ext = mimestuff.lookup.guess_extension(i.data_type)
            elif self.__type == 'icon':
                ext = mimestuff.lookup.guess_extension(i.icon_type)
            elif self.__type == 'submit':
                ext = '.cgi'

        if not ext:
            ext = '.dat'

	return "%s/%s%s" % (hash, str(self), ext)

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

	    'request': self.__request,
	    }

	return MineKey(**foo)

    def spawn_iid(self, iid):
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

    def spawn_submit_self(self):
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
	retval.__depth = 1 # forced to 1, hence check above
	retval.validate() # if we futz with it, we must validate
	return retval

    ##################################################################

    # THIS NEEDS A REWRITE
    # THIS NEEDS A REWRITE
    # THIS NEEDS A REWRITE

    html_re = re.compile(r"""(SRC|HREF)\s*=\s*(['"]?)/api/(DATA|ICON)/(\d+)([^\s\>]*)""", re.IGNORECASE)

    # THIS NEEDS A REWRITE
    # THIS NEEDS A REWRITE
    # THIS NEEDS A REWRITE

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
        with the results of self.spawn_iid(iid).permalink() - in other
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

        if the URL does NOT begine with a quote characer, the rewriter
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
                rewrite = self.spawn_iid(iid).permalink()
            elif what == 'icon':
                rewrite = self.spawn_icon(iid).permalink()
            else:
                return mo.group(0)

            return '%s="%s"' % (action, rewrite)

        return self.html_re.sub(rewrite_link, html)

##################################################################

if __name__ == '__main__':
    foo = {
	'type': 'data',
	'fid': 42,
	'fversion': 1,
	'iid': 69,
	'depth': 3,
	}

    mk = MineKey(**foo)
    print mk
    print mk.key()
    print mk.permalink()

    x = mk.spawn_submit_self()
    print x
    print x.permalink()

    y = mk.spawn_iid(100)
    print y
    print y.permalink()

    print y.spawn_submit_self()
    
    print mk.rewrite_html('--<A HREF="/api/data/11">foo</A>--')
    print mk.rewrite_html('--<A HREF="/api/icon/11">foo</A>--')

    print mk.rewrite_html('--<A HREF="/api/data/12" >foo</A>--')
    print mk.rewrite_html('--<A HREF="/api/icon/12" >foo</A>--')

    print mk.rewrite_html('--<A HREF="/api/data/13/">foo</A>--')
    print mk.rewrite_html('--<A HREF="/api/icon/13/">foo</A>--')

    print mk.rewrite_html('--<A HREF="/api/data/14/bar">foo</A>--')
    print mk.rewrite_html('--<A HREF="/api/icon/14/bar">foo</A>--')

    print mk.rewrite_html('--<A HREF="/api/data/15/bar" >foo</A>--')
    print mk.rewrite_html('--<A HREF="/api/icon/15/bar" >foo</A>--')

    print mk.rewrite_html('--<A HREF="/api/data/16/bar" x>foo</A>--')
    print mk.rewrite_html('--<A HREF="/api/icon/16/bar" x>foo</A>--')

    print mk.rewrite_html('--<A HREF="/api/data/17/bar\' x>foo</A>--')
    print mk.rewrite_html('--<A HREF="/api/icon/17/bar\' x>foo</A>--')

    print mk.rewrite_html('--<A HREF="/API/DATA/18">FOO</A>--')
    print mk.rewrite_html('--<A HREF="/API/ICON/18">FOO</A>--')

    a = """
<A HREF="/api/data/20/bar">foo</A>
<A HREF="/api/data/21/bar">foo</A>
<A HREF="/api/data/22/bar">foo</A>
"""

    print mk.rewrite_html(a)
