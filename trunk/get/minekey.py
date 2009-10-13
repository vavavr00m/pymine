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

import base64
import hashlib
import re

# using pycrypto 2.0.1
# http://www.amk.ca/python/code/crypto (old)
# http://www.pycrypto.org/ (new)
from Crypto.Cipher import AES

from pymine.api.models import Relation

class MineKey:
    key_magic = 'py1' # recognise these keys
    corefmt = '%s,%d,%d,%d,%d,%s'
    valid_methods = ( 'get', 'put' )

    b64_alt = '!@'

    aes_mode = AES.MODE_CBC
    aes_key = '1234567890123456' # 128 bits
    aes_iv =  'abcdefghijklmnop' # 128 bits

    # should we be worried that href="1' - will match?
    html_re = re.compile(r"""(SRC|HREF)\s*=\s*(['"]?)(\d+)([^\s\>]*)""", re.IGNORECASE)

    def __init__(self, **kwargs):
	# flush through with invalid data
	self.method = kwargs.get('method', None)
	self.rid = kwargs.get('rid', -1)
	self.rvsn = kwargs.get('rvsn', -1)
	self.iid = kwargs.get('iid', -1)
	self.depth = kwargs.get('depth', -1)

    @classmethod
    def b64e(self, x):
	return base64.b64encode(x, self.b64_alt)

    @classmethod
    def b64d(self, x):
	return base64.b64decode(x, self.b64_alt)

    @classmethod
    def hashify(self, x):
	m = hashlib.md5() # more than adequate
	m.update(x)
	h = m.digest()
	return self.b64e(h).rstrip('=')

    @classmethod
    def crypto_engine(self):
	return AES.new(self.aes_key, self.aes_mode, self.aes_iv)

    @classmethod
    def encrypt(self, x):
	l = len(x)
	if (l % 16): # if not a 16-byte message, pad with whitespace
	    y =  '%*s' % (-(((l // 16) + 1) * 16), x)
	else: # we got lucky
	    y = x
	engine = self.crypto_engine()
	return engine.encrypt(y)

    @classmethod
    def decrypt(self, x):
	engine = self.crypto_engine()
	return engine.decrypt(x).rstrip() # remove whitespace padding

    def validate(self):
	if self.rid <= 0:
	    raise RuntimeError, 'negative or zero rid: ' + str(self.rid)

	if self.rvsn <= 0:
	    raise RuntimeError, 'negative or zero rvsn: ' + str(self.rvsn)

	if self.iid < 0:
	    raise RuntimeError, 'negative iid: ' + str(self.iid)

	if self.depth < 0:
	    raise RuntimeError, 'negative depth: ' + str(self.depth)

	if self.method not in self.valid_methods:
	    raise RuntimeError, 'bad method: ' + str(self.method)

    def clone(self):
	retval = MineKey(method=self.method,
			 rid=self.rid,
			 rvsn=self.rvsn,
			 iid=self.iid,
			 depth=self.depth,
			 )
	retval.validate()
	return retval

    @classmethod
    def parse(self, external):
	encrypted = self.b64d(external.encode('utf-8')) # stuff comes from URLs in UNICODE
	internal = self.decrypt(encrypted)

	(Xhash, Xmethod, Xrid, Xrvsn, Xiid, Xdepth, Xkey_magic) = internal.split(',', 7)

	if Xkey_magic != self.key_magic: # eventually switch, here
	    raise RuntimeError, 'failed magic validation'

	# Xhash computed string
	# Xmethod string
	Xrid = int(Xrid)
	Xrvsn = int(Xrvsn)
	Xiid = int(Xiid)
	Xdepth = int(Xdepth)
	# Xkey_magic constant string

        # see also __str__()
	core = self.corefmt % (Xmethod, 
                               Xrid, 
                               Xrvsn, 
                               Xiid, 
                               Xdepth, 
                               Xkey_magic)

	hash2 = self.hashify(core)

	if Xhash != hash2:
	    raise RuntimeError, "failed hash validation"

	retval = MineKey(method=Xmethod,
			 rid=Xrid,
			 rvsn=Xrvsn,
			 iid=Xiid,
			 depth=Xdepth,
			 )
	retval.validate()

	return retval

    def __str__(self):
	args = (self.method,
		self.rid,
		self.rvsn,
		self.iid,
		self.depth,
		self.key_magic, # class
		)

	core = self.corefmt % args
	hash = self.hashify(core) # compute hash over core
	return "%s,%s" % (hash, core)

    def permalink(self):
        return "/get/" + self.key() # TODO; fix

    def key(self):
	internal = str(self)
	encrypted = self.encrypt(internal)
	external = self.b64e(encrypted)
	return external

    @classmethod
    def feed_for(self, rid):
	rvsn = 1 # TODO: lookup
	retval = MineKey(method='get',
			 rid=rid,
			 rvsn=rvsn,
			 iid=0,
			 depth=3,
			 )
	retval.validate()
	return retval

    def spawn_iid(self, iid):
	retval = self.clone()
	retval.iid = iid
	retval.depth -= 1
	retval.validate()
	return retval

    def rewrite_html(self, html):
        def rewrite_link(mo):
            action = mo.group(1)
            fq = mo.group(2)
            iid = int(mo.group(3))
            lq = mo.group(4)
            if fq != lq: return mo.group(0)
            return '%s="%s"' % (action, self.spawn_iid(iid).permalink())
        return self.html_re.sub(rewrite_link, html)

    def validate_against(self, request, want_method):

        # check get vs put
        if self.method != want_method:
            raise RuntimeError, "minekey is wrong method: " + str(mk)

        # check depth
        if self.depth <= 0:
            raise RuntimeError, "minekey has run out of depth: " + str(mk)

        # check global ToD restrictions
        # TODO

        # load relation
        try:
            r = Relation.objects.get(id=self.rid)
        except Relation.DoesNotExist, e:
            raise RuntimeError, "relation is not valid: " + str(mk)

        # check rvsn
        if r.version != self.rvsn:
            raise RuntimeError, "minekey/relation version mismatch: " + str(mk)

        # check against relation IP address
        if r.network_pattern:
            if 'REMOTE_ADDR' not in request.META:
                raise RuntimeError, "relation specifies network pattern but REMOTE_ADDR unavailable: " + str(r)

            src = request.META.get('REMOTE_ADDR')

            # this is hardly CIDR but can be fixed later
            if not src.startswith(r.network_pattern):
                raise RuntimeError, "relation being accessed from illegal REMOTE_ADDR: " + src

        # check ToD against relation embargo time

        if r.embargo_before:
            pass # TODO

        if r.embargo_after:
            pass # TODO

        # check if the non-feed item is marked "not:relationName"
        if self.iid:
            pass # TODO

        # ok, we're happy.

##################################################################

if __name__ == '__main__':
    m1 = MineKey(method='get', rid=1, rvsn=1, iid=1, depth=2)
    print "orig: ", m1, m1.key()

    m2 = MineKey.parse(m1.key())
    print "parse:", m2, m2.key()

    m3 = MineKey.feed_for(2)
    print "feed2:", m3, m3.key()

    m4 = m3.spawn_iid(69)
    print "spawn:", m4, m4.key()

    m5 = m4.spawn_iid(42)
    print "spawn:", m5, m5.permalink()

    h1 = """
<A HREF="99">a link to item 99</A> 
and <A src="99">again</A>
and <A HREF="99">again</A>
and <A HREF='99'>again</A>
and <A HREF=99>again</A>
and <A HREF=98>again</A>

and <A HREF="99'>this should fail "x'</A>
and <A HREF='99">this should fail "x'</A>

and <A HREF='99>this should fail 'x</A>
and <A HREF="99>this should fail "x</A>
and <A HREF=99'>this should fail x'</A>
and <A HREF=99">this should fail x"</A>
and <A HREF=99.xml>this should fail 99.xml</A>

"""

    print m3.rewrite_html(h1)

    m3.validate_against({}, 'get')
