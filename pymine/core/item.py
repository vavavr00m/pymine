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

##################################################################

class Item(Thing):

    """..."""

    booted = False # must set this to false in the definition of every subclass
    keyPrefix = 'item'
    keyRegexp = '^item[A-Z]'
    keyNamesUnique = False
    # -> keysuffix : ( isReadWrite, isRequired, isOneLine, isVirtual, ArgTuple )
    keySettings = {
	'Id' : ( False, True, True, True, None, 'unique numeric identifier for this item' ),
	'Name' : ( True, True, True, False, None, 'optional name for this item' ),
	'Status' : ( True, True, True, False, ( 0, 1, 2 ), 'status of this item (private, shared, public)' ),
	'Description' : ( True, False, True, False, None, 'optional description for this item (multiline, HTML)' ),
	'HideBefore' : ( True, False, True, False, None, 'optional date before which this object is hidden from others' ),
	'HideAfter' : ( True, False, True, False, None, 'optional date after which this object is hidden from others' ),
	'Tags' : ( True, False, True, False, None, 'optional tags describing this item (tags must already exist)' ),
	'Type' : ( True, False, True, False, None, 'HTTP mime-type relevant to this item' ),
	}

    # itemStatus ArgTuple:
    # 0: private
    # 1: shared
    # 2: public
    # 3: reserved0
    # 4: reserved1
    # 5: reserved2
    # 6: reserved3
    # 7: reserved4

    def __init__(self, aggregator, id):
	"""..."""
	Thing.__init__(self, aggregator, id)

##################################################################

class Items(Things):

    """..."""

    subpath = "items"
    genclass = Item

    def __init__(self, mine):
	"""..."""
	Things.__init__(self, mine)
	pass
