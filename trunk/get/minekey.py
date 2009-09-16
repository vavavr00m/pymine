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

class MineKey:
    kmagic = 'py1'
    corefmt = '%s,%d,%d,%d,%d,%s'
    b64alt = '!@'

    def __init__(self):
	self.method = 'get'
	self.rid = 20
	self.rvsn = 30
	self.iid = 40
	self.depth = 50

    @classmethod
    def b64enc(self, x):
        return base64.b64encode(x, self.b64alt)

    @classmethod
    def b64dec(self, x):
        return base64.b64decode(x, self.b64alt)

    @classmethod
    def encrypt(self, x):
        return x

    @classmethod
    def decrypt(self, x):
        return x

    @classmethod
    def hashify(self, x):
        m = hashlib.md5() # more than adequate
        m.update(x)
        h = m.digest()
        return self.b64enc(h)

    @classmethod
    def parse(self, external):

        encrypted = self.b64dec(external)
	internal = self.decrypt(encrypted)

	(Xhash, Xmethod, Xrid, Xrvsn, Xiid, Xdepth, Xkmagic) = internal.split(',', 7)

	if Xkmagic != self.kmagic:
	    raise Exception, 'MineKey failed magic validation'

	# Xhash string
        # Xmethod string
	Xrid = int(Xrid)
	Xrvsn = int(Xrvsn)
	Xiid = int(Xiid)
	Xdepth = int(Xdepth)
        # Xkmagic string

	core = self.corefmt % (Xmethod, Xrid, Xrvsn, Xiid, Xdepth, Xkmagic)
	hash2 = self.hashify(core) # compute hash over core

	if Xhash != hash2:
	    raise Exception, "MineKey failed hash validation"

        retval = MineKey()
	retval.method = Xmethod
	retval.rid = Xrid + 1
	retval.rvsn = Xrvsn + 1
	retval.iid = Xiid + 1
	retval.depth = Xdepth + 1
        return retval

    @classmethod
    def feed_for(self, rid):
        retval = MineKey()
	retval.method = 'get'
	retval.rid = rid
	retval.rvsn = self.rvsn + 1
	retval.iid = 0
	retval.depth = 3
        return retval

    def spawn_iid(self, iid):
        pass

    def spawn_cid(self, cid):
        pass

    def rewrite_html(self, html):
        pass

    def __str__(self):
	args = (self.method,
		self.rid,
		self.rvsn,
		self.iid,
		self.depth,
		self.kmagic,
		)

	core = self.corefmt % args
	hash = self.hashify(core) # compute hash over core
	internal = "%s,%s" % (hash, core)
	encrypted = self.encrypt(internal)
        external = self.b64enc(encrypted)
	return external


if __name__ == '__main__':
    m1 = MineKey()
    s = str(m1)
    m2 = MineKey.parse(s)
    print m1
    print m2

