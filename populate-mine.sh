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
./mineauth.sh login

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

# set up some relations
Minectl new-relation alec 1 "Alec Muffett" food drink except:spirits animals themineproject
Minectl new-relation adriana 1 "Adriana Lukas" food drink shoes cats motorcycles themineproject
Minectl new-relation carrie 1 "Carrie Bishop" food drink sneakers themineproject
Minectl new-relation ben 1 "Ben Laurie" food drink cats motorcycles
Minectl new-relation perry 1 "Perry deHavilland" hippos red-wine

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
    Minectl create-comment $item commentRelation=$who commentTitle=$what commentBody="$body"
done <<EOF
1 adriana title1 this is body 1
1 alec title2 this is body 2
1 carrie title3 this is body 3
2 perry title4 this is body 4
2 perry title5 this is body 5
3 ben title6 this is body 5
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
private for:alec
private for:ben
private for:carrie
private for:perry
public animals
public food not:carrie
public for:adriana
public for:alec
public for:ben
public for:carrie
public for:carrie not:ben
public for:carrie not:carrie
public for:perry
public red-burgundy not:perry
public rioja
shared for:adriana
shared for:alec
shared for:ben
shared for:carrie
shared for:perry
EOF

while read name status type tag description
do

    Minectl create-item \
	"itemName=$name" \
	"itemStatus=$status" \
	"itemTags=$tag" \
	"itemType=$type" \
	"itemDescription=$description"

done <<EOF
example-dataless-item public text/html themineproject this is an extended description which will turn up as data
EOF

# done
exit 0
