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
    ./minectl.pl -vve "$@"
}


exec 2>&1
set -x

###
# set up some very general tags

# concepts
Minectl new-tags animals clothes countryside drink space \
         fashion food friends plants transport travel

# countries
Minectl new-tags france spain italy usa

# geekery
Minectl new-tags themineproject

###
# set up some implied tags; cats imply animals, motorbikes imply transport, ...

Minectl new-tags cats:animals dogs:animals birds:animals hippos:animals
Minectl new-tags flowers:plants vegetables:plants trees:plants
Minectl new-tags bicycles:transport motorbikes:transport cars:transport

###
# set up tags and implied tags in one go; read from left to right

Minectl new-tags wine:drink beer:drink 
Minectl new-tags white-wine:wine red-wine:wine chardonnay:white-wine rioja:red-wine

###
# for shoe-fetishists "shoes" implies BOTH clothes AND fashion

Minectl new-tags shoes:clothes,fashion

# shoe types

Minectl new-tags \
    mules:shoes \
    pumps:shoes \
    slingbacks:shoes \
    sneakers:shoes \
    stilettos:shoes \
    trainers:shoes

###
# set up some relations

Minectl new-relation alec 1 "Alec Muffett" cats motorbikes drink food themineproject
Minectl new-relation adriana 1 "Adriana Lukas" wine motorbikes themineproject
Minectl new-relation carrie 1 "Carrie Bishop" sneakers trainers themineproject
Minectl new-relation ben 1 "Ben Laurie" wine food motorbikes
Minectl new-relation perry 1 "Perry de Havilland" food drink except:white-wine

##################################################################
##################################################################
##################################################################

exit 0

###
# upload a batch of objects without individual tagging

Minectl upload -s public $SAMPLES/* # wasn't that easy?

###
# highly verbose special cases for tag testing
while read file tags
do
    Minectl upload -s public -t "$tags" $SAMPLES/$file
done <<EOF
adriana.jpg themineproject
alecm.png themineproject
austen.txt
bridge.jpg countryside
buster.jpg cats
cloud.jpg
dam.jpg countryside 
fashion1.jpg fashion
feeds-based-vrm.pdf themineproject
italy.jpg italy
milan.jpg italy
mine-diagram.jpg themineproject
mine-paper-v2.pdf themineproject
monument.jpg france motorbikes countryside
moon.jpg space
mountains.jpg  italy motorbikes countryside
pimpernel.jpg flowers
rome.jpg italy
rose.jpg flowers
stonehenge.jpg countryside
suzi.jpg cats
woodland.jpg trees countryside
EOF

###
# done

exit 0
