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

#from types import *
from xml.sax.saxutils import escape

def __space(buffer):
    buffer.append(' ')

def __newline(buffer):
    buffer.append('\n')

def __indent(buffer, depth):
    buffer.append(depth * '  ')

def __push(buffer, token):
    buffer.append(token)

def __descend(buffer, depth, *arguments):
    for arg in arguments:

	if isinstance(arg, int) \
                or isinstance(arg, long) \
                or isinstance(arg, float) \
                or isinstance(arg, bool):
	    __push(buffer, str(arg))
	    return False

	elif isinstance(arg, str):
	    __push(buffer, escape(arg))
	    return False

	elif isinstance(arg, unicode):
	    __push(buffer, escape(arg.encode('utf-8')))
	    return False

	elif isinstance(arg, tuple) or isinstance(arg, list):
	    trip = False
	    for v in arg:
		if trip and not isinstance(v, dict): 
                    __space(buffer)
		__descend(buffer, depth, v)
		trip = True
	    return False

	elif isinstance(arg, dict):
	    keys = arg.keys()
	    keys.sort()
	    for k in keys:
		v = arg[k]

		__indent(buffer, depth)
		__push(buffer, '<%s>' % k)

		nested = (isinstance(v, dict) or \
                              (isinstance(v, list) and isinstance(v[0], dict)))

                if nested:
		    __newline(buffer)

		if __descend(buffer, depth+1, arg[k]) or nested:
		    __indent(buffer, depth)

		__push(buffer, '</%s>' % k)
		__newline(buffer)

	    return True

	else:
	    raise RuntimeError, 'unknown type for argument %s %s' % (str(arg), type(arg))

def dumps(foo):
    """
    Quick and dirty XML serialisation for data structures, 
    wrapping them in an "envelope" object.
    """
    buffer = []
    env = { 'envelope': foo }
    __descend(buffer, 0, env)
    return "".join(buffer)

if __name__ == '__main__':
    foo = {
	'integer': 42,
	'string': 'this is a string',
	'list': (1, 2, 3),
        'html': '<foo>bar&baz</foo>',
        'complex': [ {'A':99}, {'B':98}, {'C':97} ],
	}
    bar = foo.copy()
    baz = foo.copy()
    bar['deep2'] = baz
    foo['deep1'] = bar
    print dumps(foo),
