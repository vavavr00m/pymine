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
Minectl new-feed alec 1 "Alec Muffett" food drink except:spirits animals themineproject
Minectl new-feed adriana 1 "Adriana Lukas" food drink shoes cats motorcycles themineproject
Minectl new-feed carrie 1 "Carrie Bishop" food drink sneakers themineproject
Minectl new-feed ben 1 "Ben Laurie" food drink cats motorcycles
Minectl new-feed perry 1 "Perry deHavilland" hippos red-wine

###
# upload a batch of objects without individual tagging

Minectl upload -t themineproject -s public $SAMPLES/*.pdf # wasn't that easy?

###
# highly verbose special cases for tag testing
while read file tags
do
    Minectl upload -s public -t "$tags" $SAMPLES/$file
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
    Minectl create-comment $item commentFeedId=$who commentTitle=$what commentBody="$body"
done <<EOF
1  1       comment-title-1  comment body  1
1  1       comment-title-2  comment body  2
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

while read status tags
do

    desc="example with status=$status tags=$tags"

    Minectl create-item \
	"itemName=example" \
	"itemDescription=$desc" \
	"itemStatus=$status" \
	"itemType=text/plain" \
	"itemTags=$tags" \
	"itemData=@$file"

done <<EOF
private for:adriana
private not:adriana
public for:adriana
public not:adriana
public not:adriana themineproject
shared for:adriana
shared not:adriana
EOF


# first iid when we go into this look is 15
while read status type name description
do
    Minectl create-item \
	"itemStatus=$status" \
	"itemType=$type" \
	"itemName=$name" \
	"itemDescription=$description"

done <<EOF
public text/html depth-0 this is a link to <a href="/api/item/16">item 16</a>
public text/html depth-1 this is a link to <a href="/api/item/17">item 17</a>
public text/html depth-2 this is a link to <a href="/api/item/18">item 18</a>
public text/html depth-3 this is a link to <a href="/api/item/19">item 19</a>
shared text/html depth-4 this is a link to <a href="/api/item/20">item 20</a>
public text/html depth-5 this is a link to <a href="/api/item/21">item 21</a>
public text/html depth-6 this is a link to <a href="/api/item/22">item 22</a>
private text/html depth-7 this is a link to <a href="/api/item/23">item 23</a>
public text/html depth-8 this is a link to <a href="/api/item/24">item 24</a>
public text/html loop this is a link to <a href="/api/item/24">item 24</a>
EOF

Minectl update-item 15 itemTags=themineproject
Minectl update-item 18 itemTags=themineproject
Minectl update-item 21 itemTags=themineproject
Minectl update-item 24 itemTags=themineproject

# audio
Minectl upload -t themineproject -s public $SAMPLES/*.mp3

# done
exit 0
