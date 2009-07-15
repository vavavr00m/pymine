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

import os
from UserDict import UserDict
from exception import MineException

##################################################################

class Thing(UserDict):

    """base class for all Mine database objects, and parent for classes of
    similar functionality below."""

    booted = False # must set this to false in the definition of every subclass
    keySuffixId = "Id"
    keySuffixName = "Name"
    keyPrefix = 'thing' # what is the prefix for keys
    keyRegexp = '^thing[A-Z]' # regexp which matches keys
    keyNamesUnique = True # are names of Things meant to be unique?

    # -> keysuffix : ( isReadWrite, isRequired, isOneLine, isVirtual, argTuple, description )
    keySettings = {
	'Id' : ( False, True, True, True, None, 'unique numeric identifier for this thing' ),
	'Name' : ( True, True, True, False, None, 'unique textual name for this thing' ),
	}

    ###
    # end of class-specific config data, but see note for Boot()

    @classmethod # <------------------------------------------------------------------ CLASSMETHOD
    def Boot(thingclass):

        """Thing and its subclasses cannot inherit class-attribute
        initialisation code, but most of it is common and need only be
        done once at class-initiation time, so this routine factors
        that code out; it MUST be run once for each Thing subclass.
        Metaclasses may sort this out but they are a big hammer to
        crack a small nut."""

        if (thingclass.booted):
            print "skipping attempt to re-boot", thingclass
            return
        else:
            print "thing.Boot for", thingclass

        thingclass.keyId = thingclass.keyPrefix + thingclass.keySuffixId # for the Id() method
        thingclass.keyName = thingclass.keyPrefix + thingclass.keySuffixName # for the Name() method

        thingclass.dictArgTuple = {}
        thingclass.dictOneLine = {}
        thingclass.dictReadWrite = {}
        thingclass.dictRequired = {}
        thingclass.dictValidKey = {}
        thingclass.dictVirtual = {}

        for suffix, ( isReadWrite, isRequired, isOneLine, isVirtual, argtup, desc ) in thingclass.keySettings.items():
            key = thingclass.keyPrefix + suffix

            print "thing.Boot configuring", thingclass, "attr", key,

            thingclass.dictValidKey[key] = desc

            if (isReadWrite): 
                thingclass.dictReadWrite[key] = True
                print "RW",
            else:
                print "RO",

            if (isRequired): 
                thingclass.dictRequired[key] = True
                print "REQD",

            if (isOneLine): 
                thingclass.dictOneLine[key] = True
                print "LINE",

            if (isVirtual):
                thingclass.dictVirtual[key] = True
                print "VIRT",

            if (argtup): 
                thingclass.dictArgTuple[key] = argtup
                print "TUPLE", argtup,

            print

        # done
        thingclass.booted = True

    @classmethod # <------------------------------------------------------------------ CLASSMETHOD
    def Describe(self, key):
	"""returns string, provides description of 'key', its meaning and usage"""
	return self.dictValidKey[key]

    ###
    # instance methods from here on down

    def __init__(self, aggregator, id):

	"""
        set up the thing object-tables; putting more code here is
        discouraged as thing-creation needs to be really cheap
        """

	UserDict.__init__(self) # we are a UserDict
	self.aggregator = aggregator # memorise my aggregator/parent
	self.id = id # and my id
        self.path = os.path.join(aggregator.path, str(id)) # where my directory is

    ##################################################################

    def RewriteForSet(self, key, value):
	"""
	Takes string 'value' and maps/processes it, returning the data
	in on-disk format for key 'key'

	In this, the superclass version which MUST be called, it
	rewrites any 'isOneLine' keys as a single line of text without
	newline and with single whitespaces.

	Blobs are left verbatim.
	"""
	if (key in self.dictOneLine): 
            value = " ".join(value.split()) # surprisingly efficient
	return value

    def Set(self, key, value): # __set_item__
	"""stores value (string) of key 'key, passing it through RewriteForSet() before storage'"""
        if (key not in self.dictValidKey):
            raise MineException("invalid key passed to set: " + key)
	pass

    ##################################################################

    def RewriteForGet(self, key, value):
	"""takes string 'value' and maps/processes it, returning the data in userland format for key 'key'"""
	return value

    def Get(self, key): # __get_item__
	"""retreives value (string) of key 'key' and returns it after passing through RewriteForGet()"""

        if (key not in self.dictValidKey):
            raise MineException("invalid key passed to Get: " + key)

	if (key in self.dictVirtual):
	    if (key == self.keyId): return str(self.id)

        fname = os.path.join(self.path, key)
        f = open(fname, "r")
        value = f.read()
        f.close()

        return self.RewriteForGet(key, value)

    ##################################################################

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

class Things:

    """
    aggregate manager for Thing objects, and parent for classes of
    similar functionality below.
    """

    subpath = "things"
    genclass = Thing

    def __init__(self, mine):
	"""setup"""

	self.mine = mine
	self.path = os.path.join(mine.path, self.subpath)

    def Create(self):
	"""Returns a new Thing, properly initialised under this Things'
	aggregator, rather than using a direct constructor.  This
	Thing /may/ not be visible to List() (etc) until Commit() is
	performed."""
	pass

    def Open(self, id):
	"""returns a Thing with id 'id'"""
        return self.genclass(self, id)

    def Exists(self, id):
	"""returns a boolean, does the Thing numbered 'id' exist?"""
	pass

    def List(self):
	"""returns a list of all Thing (ie: list of Thing objects) known to this Thing aggregator"""
	pass

    def ListIds(self):
	"""returns a list of all Thing.id (ie: list of int) known to this Thing aggregator"""
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
