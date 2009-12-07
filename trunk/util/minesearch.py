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

"""
code to parse mine search queries and return a useful structure
"""

def parse(input):
    """
    tokenises string and create a dict of lists of tuple.

    the dict has three keys: 'require', 'query', 'exclude'

    the inner tuples parse stuff like "foo:bar" yielding ('foo','bar')

    where no 'foo:' is given, the 'token' is used.
    """
    retval = {
        'query': [],
        'require': [],
        'exclude': [],
        }

    for token in input.split():
        if token.startswith('+'):
            destination = 'require'
            token = token[1:]
        elif token.startswith('-'):
            destination = 'exclude'
            token = token[1:]
        else:
            destination = 'query'

        i = token.find(':')

        if i >= 0:
            key = token[0:i]
            value = token[i+1:]
        else:
            key = 'token'
            value = token

        retval[destination].append((key,value))

    return retval


if __name__ == '__main__':

    for i in ('foo', 
              'foo +bar -baz', 
              'foo +bar -baz type:audio/mp3 +inname:wibble -size:-100k', 
              'foo: +bar: -baz:',
              ):
        print i
        print str(parse(i))
        print 
