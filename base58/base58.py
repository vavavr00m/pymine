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

# spec: http://www.flickr.com/groups/api/discuss/72157616713786392/

b58chars = '123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ'
b58base = len(b58chars) # mildly redundant

def b58encode(value):
    encoded = ''
    while value >= b58base:
        div, mod = divmod(value, b58base)
        encoded = b58chars[mod] + encoded # add to left
        value = div
    encoded = b58chars[value] + encoded # most significant remainder
    return encoded

def b58decode(encoded):
    value = 0
    column_multiplier = 1;
    for c in encoded[::-1]:
        column = b58chars.index(c)
        value += column * column_multiplier
        column_multiplier *= b58base
    return value

if __name__ == '__main__':
    x = b58encode(12345678)
    print x, '26gWw'
    print b58decode(x), 12345678
