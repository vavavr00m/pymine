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
import util.base64_mine as b64
import getopt
import os
import sys

from api.models import Registry

def initialise_crypto():
    nbytes = 256/8
    mine_hmac_key = b64.encode(os.urandom(nbytes))
    mine_hmac_pad = b64.encode(os.urandom(nbytes))
    Registry.set_encoded('__MINE_HMAC_KEY__', mine_hmac_key, False)
    Registry.set_encoded('__MINE_HMAC_PAD__', mine_hmac_pad, False)
 
def create_user(username, password):
    u = User()
    u.username = username
    u.set_password(password)
    u.save()

def usage():
    print "usage:"
    print "\tinit-crypto # call only once"
    print "\tcreate-user username password"
    print "\tset key value [0|1] # 1 to permit overwrites"
    print "\tset-encoded key value [0|1] # 1 to permit overwrites"

def main(argv):
    cmds = {
        'create-user': create_user,
        'init-crypto': initialise_crypto,
        'set': Registry.set,
        'set-encoded': Registry.set_encoded,
        }
    fn = cmds.get(argv[0], usage)
    fn(*argv[1:])

if __name__ == "__main__":
    main(sys.argv[1:])
