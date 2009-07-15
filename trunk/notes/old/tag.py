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

class Tag(Thing):

    """..."""
    booted = False # must set this to false in the definition of every subclass
    keyPrefix = 'tag'
    keyRegexp = '^tag[A-Z]'
    keyNamesUnique = True
    # -> keysuffix : ( isReadWrite, isRequired, isOneLine, isVirtual, ArgTuple )
    keySettings = {
	'Id' : ( False, True, True, True, None, 'numeric identifier for this tag' ),
	'Implied' : ( True, False, True, False, None,
                      """list of more general tags implied by this one, eg: 'cheese' tag may imply 'food' tag""" ),
	'Name' : ( True, True, True, False, None, 'unique alphanumeric tagname' ),
	}

    def __init__(self, aggregator, id):
	"""..."""
	Thing.__init__(self, aggregator, id)

##################################################################

class Tags(Things):

    """..."""

    subpath = "tags"
    genclass = Tag

    def __init__(self, mine):
	"""..."""
	Things.__init__(self, mine)
	pass
