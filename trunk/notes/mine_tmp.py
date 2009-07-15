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

# Notation:
# ALLCAPS() -> class or static method/attribute
# InitialCapital() -> instance method
# initialLowercase -> instance attribute

import os
from UserDict import UserDict

class Mine:
    """the master container-object for a per-username Mine"""

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

##################################################################

class Cache:
    def __init__(self, mine):
	"""setup"""
	self.mine = mine

    def get(self, wotsit):
	pass

    def put(self, wotsit):
	pass

##################################################################

class Things:

    """
    aggregate manager for Thing objects, and parent for classes of
    similar functionality below.
    """

    subpath = "things" # probably does not exist

    def __init__(self, mine):
	"""setup"""

	self.mine = mine
	self.path = os.path.join(mine.path, self.subpath)

    def New(self):
	"""
	Returns a new Thing, properly initialised under this Things
	aggregator, rather than using a direct constructor.

	This Thing /may/ not be visible to List() (etc) until Commit()
	is performed
	"""
	pass

    def ListIds(self):
	"""returns a list of all Thing.id (ie: list of int) known to this Thing aggregator"""
	pass

    def List(self):
	"""returns a list of all Thing (ie: list of Thing objects) known to this Thing aggregator"""
	pass

    def Exists(self, id):
	"""returns a boolean, does the Thing numbered 'id' exist?"""
	pass

    def Named(self, name):
	"""returns a list of Thing, of name 'name'; returns empty list if no match"""
	pass

    def NamedSingle(self, name):
	"""returns a single Thing of name 'name'; raises exception if multiple identical names are permitted or found"""
	pass

    def Select(self, srchw):
	"""returns a list of Thing matching SearchWotsit 'srchw'"""
	pass

    def Freeze(self):
	"""locks this Things object against addition/deletion"""
	pass

    def Thaw(self):
	"""unlocks this Things object, see 'Freeze'"""
	pass

##################################################################

class Thing(UserDict):

    """base class for all Mine database objects, and parent for classes of
    similar functionality below."""

    keyPrefix = 'thing' # what is the prefix for keys
    keyRegexp = '^thing[A-Z]' # regexp which matches keys
    keyNamesUnique = True # are names of Things meant to be unique?
    # -> keysuffix : ( isReadOnly, isRequired, isOneLine, isVirtual, enumeration )
    keySettings = {
	'Id' : ( True, True, True, True, None ),
	'Name' : ( False, True, True, False, None ),
	}

    ###
    # end of class-specific config data, but see note for BOOT()

    @classmethod
    def BOOT(tclass):

        """Thing and its subclasses cannot inherit class-attribute
        initialisation code, but most of it is common and need only be
        done once at class-initiation time, so this routine factors
        that code out; it MUST be run once for each Thing
        subclass..."""

        tclass.keyId = tclass.keyPrefix + "Id" # for the Id() method
        tclass.keyName = tclass.keyPrefix + "Name" # for the Name() method

        tclass.dictEnumeration = {}
        tclass.dictOneLine = {}
        tclass.dictReadOnly = {}
        tclass.dictRequired = {}
        tclass.dictValidKey = {}
        tclass.dictVirtual = {}

        for suffix, ( isReadOnly, isRequired, isOneLine, isVirtual, enumtuple ) in tclass.keySettings.items():
            key = tclass.keyPrefix + suffix
            tclass.dictValidKey[key] = True
            if (isReadOnly): tclass.dictReadOnly[key] = True
            if (isRequired): tclass.dictRequired[key] = True
            if (isOneLine): tclass.dictOneLine[key] = True
            if (isVirtual): tclass.dictVirtual[key] = True
            if (enumtuple): tclass.dictEnumeration[key] = enumtuple

    ###
    # instance methods from here on down

    def __init__(self, parent, id):

	"""set up the thing object-tables"""

	UserDict.__init__(self) # we are a UserDict
	self.parent = parent # memorise my aggregator/parent
	self.mine = parent.mine # memorise my mine
	self.id = id # and my id

    def MapOutbound(self, key, value):
	"""
	Takes string 'value' and maps/processes it, returning the data
	in on-disk format for key 'key'

	In this, the superclass version which MUST be called, it
	rewrites any 'isOneLine' keys as a single line of text without
	newline and with single whitespaces.

	Blobs are left verbatim.
	"""
	if (key in self.dictOneLine): value = " ".join(value.split())
	return value

    def Set(self, key, value): # __set_item__
	"""stores value (string) of key 'key, passing it through MapOutbound() before storage'"""
	pass

    # ----

    def MapInbound(self, key, value):
	"""takes string 'value' and maps/processes it, returning the data in userland format for key 'key'"""
	return value

    def Get(self, key): # __get_item__
	"""retreives value (string) of key 'key' and returns it after passing through MapInbound()"""

	if (key in self.dictVirtual):
	    if (key == self.keyId): return str(self.id)

    # ----


    def Id(self):
	"""returns this Thing's id (integer > 0)"""
	return self.Get(keyId)

    def Name(self):
	"""returns this Thing's name (string)"""
	return self.Get(keyName)

    def Keys(self):
	"""returns a list of keys (string) for this Thing"""
	pass

    def Commit(self):
	"""
	Ensures the state of this Thing is written to disk; the mode
	of update is implementation dependent (params may be written
	to disk synchronously without Commit) but use of Commit is
	mandatory to ensure updates.

	Raises an exception on failure.

	Note: implementations should strive to implement atomic Set()
	"""
	pass

    def Delete(self):
	"""deletes this Thing or raises an exception"""
	pass

    def Has(self, key):
	"""returns boolean, does this Thing have a key named 'key'"""
	return True

    def Compare(self, thing): # __cmp__
	"""compares one Thing with another, implements __cmp__ semantics"""
	pass

    def Printable(self): # -> __repr__
	"""supplies a Printable representation of a Thing, implements __repr_ semantics"""
	pass

    def Meta(self):
	"""returns a ThingMeta object for this Thing, providing useful metainformation"""
	pass

    def Lock(self):
	"""locks this Thing against amendment"""
	pass

    def Unlock(self):
	"""unlocks this Thing (see Lock)"""
	pass



##################################################################
##################################################################
##################################################################

class Tags(Things):

    """..."""

    subpath = "tags"

    def __init__(self, mine):
	"""..."""
	Things.__init__(self, mine)
	pass

##################################################################

class Tag(Thing):

    """..."""
    keyPrefix = 'tag'
    keyRegexp = '^tag[A-Z]'
    keyNamesUnique = True
    # -> keysuffix : ( isReadOnly, isRequired, isOneLine, isVirtual, enumeration )
    keySettings = {
	'Id' : ( True, True, True, True, None ),
	'Name' : ( False, True, True, False, None ),
	}

    def __init__(self, parent):
	"""..."""
	Thing.__init__(self, parent)
	pass

##################################################################
##################################################################
##################################################################

class Relations(Things):

    """..."""

    subpath = "relations"

    def __init__(self, mine):
	"""..."""
	Things.__init__(self, mine)
	pass

##################################################################

class Relation(Thing):

    """..."""
    keyPrefix = 'relation'
    keyRegexp = '^relation[A-Z]'
    keyNamesUnique = True
    # -> keysuffix : ( isReadOnly, isRequired, isOneLine, isVirtual, enumeration )
    keySettings = {
	'Id' : ( True, True, True, True, None ),
	'Name' : ( False, True, True, False, None ),
	}

    def __init__(self, parent):
	"""..."""
	Thing.__init__(self, parent)
	pass

##################################################################
##################################################################
##################################################################

class Items(Things):

    """..."""

    subpath = "items"

    def __init__(self, mine):
	"""..."""
	Things.__init__(self, mine)
	pass

##################################################################

class Item(Thing):

    """..."""
    keyPrefix = 'item'
    keyRegexp = '^item[A-Z]'
    keyNamesUnique = False
    # -> keysuffix : ( isReadOnly, isRequired, isOneLine, isVirtual, enumeration )
    keySettings = {
	'Id' : ( True, True, True, True, None ),
	'Name' : ( False, True, True, False, None ),
	'Status' : ( False, True, True, False, ( 0, 1, 2 ) ),
	}

    # itemStatus enumeration:
    # 0: private
    # 1: semiprivate
    # 2: private
    # 3: reserved0
    # 4: reserved1
    # 5: reserved2
    # 6: reserved3
    # 7: reserved4

    def __init__(self, parent):
	"""..."""
	Thing.__init__(self, parent)
	pass

##################################################################
##################################################################
##################################################################

class Comments(Things):

    """..."""

    subpath = ".../comments" # fix this

    def __init__(self, mine):
	"""..."""
	Things.__init__(self, mine)
	pass

##################################################################

class Comment(Thing):

    """..."""
    keyPrefix = 'comment'
    keyRegexp = '^comment[A-Z]'
    keyNamesUnique = False
    # -> keysuffix : ( isReadOnly, isRequired, isOneLine, isVirtual, enumeration )
    keySettings = {
	'Id' : ( True, True, True, True, None ),
	'Name' : ( False, True, True, False, None ),
	}

    def __init__(self, parent):
	"""..."""
	Thing.__init__(self, parent)
	pass

##################################################################
##################################################################
##################################################################

class Config(Thing):

    """..."""
    keyPrefix = 'config'
    keyRegexp = '^config[A-Z]'
    keyNamesUnique = True
    # -> keysuffix : ( isReadOnly, isRequired, isOneLine, isVirtual, enumeration )
    keySettings = {
	'Id' : ( True, True, True, True, None ),
	'Name' : ( False, True, True, False, None ),
	}

    def __init__(self, mine):
	"""..."""
	Thing.__init__(self, mine, 0)
	pass

##################################################################
##################################################################
##################################################################

class MineKey():

    """..."""

    def __init__(self):
	"""..."""
	pass

##################################################################

class ThingMeta:

    """Container object that provides platform meta-information about a Thing."""

    lastmodified = None
    created = None
    size = None
    path = None
    name = None
    type = None

    def __init__(self):
	"""..."""
	pass

##################################################################

class RequestWotsit:
    """..."""
    def __init__(self):
	"""..."""
	pass

##################################################################

class SearchWotsit:
    """..."""
    def __init__(self):
	"""..."""
	pass

##################################################################

class CryptoEngine:
    """..."""
    def __init__(self):
	"""..."""
	pass

##################################################################


##################################################################

if __name__ == '__main__':

    Thing.BOOT()
    Tag.BOOT()
    Relation.BOOT()
    Item.BOOT()
    Comment.BOOT()

    mine = Mine("alecm")

    print Thing.dictValidKey
    print Tag.dictValidKey
    print Relation.dictValidKey
    print Item.dictValidKey
    print Item.dictEnumeration
    print Comment.dictValidKey
