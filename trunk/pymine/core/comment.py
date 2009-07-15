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

class Comment(Thing):

    """..."""

    booted = False # must set this to false in the definition of every subclass
    keySuffixName = 'Subject'
    keyPrefix = 'comment'
    keyRegexp = '^comment[A-Z]'
    keyNamesUnique = False
    # -> keysuffix : ( isReadWrite, isRequired, isOneLine, isVirtual, ArgTuple )
    keySettings = {
	'Id' : ( False, True, True, True, None, 'unique numeric identifier for this comment (under this object)' ),
	'Subject' : ( True, False, True, False, None, 'optional subject line for this comment' ),
	'Body' : ( True, False, False, False, None, 'optional body for this comment (multiline, HTML)' ),
	'RelationId' : ( True, True, True, False, None, 'relationId for the creator of this comment' ),
	}

    def __init__(self, aggregator, id):
	"""..."""
	Thing.__init__(self, aggregator, id)
	pass

##################################################################

class Comments(Things):

    """..."""

    subpath = None
    genclass = Comment

    def __init__(self, mine, itemid):
	"""..."""
        subpath = os.path.join("items", str(itemid), "comments")
	Things.__init__(self, mine)
