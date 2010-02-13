#!/bin/sh

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

Minectl() {
    ./minectl.pl -xe "$@"
}

SAMPLES=public_html/testdata
exec 2>&1
set -x

# login
./mine-auth-wrapper.sh login

# set up some very general tags
Minectl new-tags themineproject literature photos

# set up tags and implied tags in one go; read from left to right
Minectl new-tags animals cats:animals dogs:animals hippos:animals

# a little more detailed
Minectl new-tags food drink motorcycles
Minectl new-tags shoes sneakers:shoes
Minectl new-tags booze:drink juice:drink
Minectl new-tags wine:booze beer:booze spirits:booze
Minectl new-tags white-wine:wine red-wine:wine
Minectl new-tags chardonnay:white-wine rioja:red-wine
Minectl new-tags red-burgundy:red-wine white-burgundy:white-wine burgundy:red-wine,white-wine # latter->both

# set up some feeds
Minectl new-feed alec 1 "Alec Muffett" food drink animals themineproject
Minectl new-feed adriana 1 "Adriana Lukas" food drink shoes cats motorcycles themineproject
Minectl new-feed carrie 1 "Carrie Bishop" food drink sneakers themineproject
Minectl new-feed ben 1 "Ben Laurie" food drink cats motorcycles
Minectl new-feed perry 1 "Perry deHavilland" hippos red-wine

###
# upload a batch of objects without individual tagging

Minectl upload -t themineproject -s sharable $SAMPLES/*.pdf # wasn't that easy?

###
# highly verbose special cases for tag testing
while read file tags
do
    Minectl upload -s sharable -t "$tags" $SAMPLES/$file
done <<EOF
adriana.jpg photos themineproject
alecm.png photos themineproject
austen.txt literature red-wine
buster.jpg photos cats
mine-diagram.jpg themineproject
EOF

# some dummy comments
while read item who what body
do
    Minectl create-comment $item commentFromFeed=$who commentTitle=$what commentBody="$body"
done <<EOF
1  alec       comment-title-1  comment body  1
1  adriana      comment-title-2  comment body  2
1  carrie  comment-title-3  comment body  3
2  perry   comment-title-4  comment body  4
2  perry   comment-title-5  comment body  5
3  ben     comment-title-6  comment body  6
EOF

# some vurls
Minectl create-vurl vurlName=mine vurlLink=http://themineproject.org/
Minectl create-vurl vurlName=alecm vurlLink=http://www.crypticide.com/dropsafe/
Minectl create-vurl vurlName=adriana vurlLink=http://mediainfluencer.net/
Minectl create-vurl vurlName=foo/bar vurlLink=http://www.google.com/
Minectl create-vurl vurlLink=http://www.google.co.uk/ # autoname

# custom objects for feed testing

file=public_html/testdata/austen.txt

# audio
Minectl upload -t themineproject -s sharable $SAMPLES/*.mp3

# done
exit 0
