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

import miner
import getpass

url = 'http://localhost:9862'
u = 'pickaxe'
p = getpass.getpass()

print "connecting to mine..."
api = miner.MineAPI(username=u, password=p, url_prefix=url)
print

print "version..."
print api.version()
print

print "list items..."
print api.list_items()
print

print "create an item..."
x = api.create_item(itemName='api test demo', itemStatus='shareable')
print x
print

print "update an item..."
iid = x['result']['item']['itemId']
y = api.update_item(iid, itemStatus='secret')
print y
print
