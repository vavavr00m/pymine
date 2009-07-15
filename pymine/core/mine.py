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

from thing import Thing, Things
from tag import Tag, Tags
from relation import Relation, Relations
from item import Item, Items
from comment import Comment, Comments
from config import Config
from cache import Cache

import os

##################################################################

class Mine:
    """the master container-object for a per-username Mine"""

    # boot the Thing classes once, and once only
    Thing.Boot()
    Tag.Boot()
    Relation.Boot()
    Item.Boot()
    Comment.Boot()
    Config.Boot()

    def __init__(self, username):
	"""initialise a mine for user 'username'"""

	# who am i?
	self.username = username

	# where shall we find the Things?
	self.path = os.path.join("database", username)

	# hack for Config to become a Thing without an aggregator
	self.mine = self

	# primary importance: configuration
	self.config = Config(self)

	# secondary importance: cache (so the rest can reference it)
	self.cache = Cache(self)

	# the remainder; items come last, and have comments beneath them
	self.tags = Tags(self)
	self.relations = Relations(self)
	self.items = Items(self)

    def Import(self, file):
	"""returns nothing, imports into a new mine the zipfile referenced by 'file'"""
	pass

    def Export(self, file, srchctx):
	"""returns a filehandle on a zipfile representing the mine with items represented by srchctx, or all if None"""
	pass

