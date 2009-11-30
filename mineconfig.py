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

"""docstring goes here""" # :-)

from django.conf import settings
from django.contrib.auth.models import User
import base64
import getopt
import os
import sys

from api.models import Registry

def set_registry(key, value, overwrite_ok):
    # as close as I can get to TAS
    r, created = Registry.objects.get_or_create(key=key, defaults={'value': value}) 

    if not created and not int(overwrite_ok):
        raise RuntimeError, 'not allowed to overwrite existing Registry key: %s' % key

    r.save()

def initialise_crypto():
    b64_alt = '!@'
    nbytes = 128/8
    mine_key = base64.b64encode(os.urandom(nbytes), b64_alt)
    mine_iv_seed = base64.b64encode(os.urandom(nbytes), b64_alt)
    set_registry('__MINE_KEY__', mine_key, False)
    set_registry('__MINE_IV_SEED__', mine_iv_seed, False)

def create_user(username, password):
    u = User()
    u.username = username
    u.set_password(password)
    u.save()
    print str(u)

def usage():
    print "usage:"
    print "\tinit-crypto # call only once"
    print "\tcreate-user username password"
    print "\tset-registry key value [0|1] # 1 to permit overwrites"

def main(argv):
    cmds = {
        'create-user': create_user,
        'init-crypto': initialise_crypto,
        'set-registry': set_registry,
        }
    fn = cmds.get(argv[0], usage)
    fn(*argv[1:])

if __name__ == "__main__":
    main(sys.argv[1:])
