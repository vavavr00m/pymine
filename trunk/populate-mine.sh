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


exec 2>&1
set -x

###
# can't be arsed to poke filenames in everywhere

SAMPLES=database/doc/sample-data

# pick up minectlopts from environment

minectl="./minectl.pl $minectlopts -e"

###
# set up some very general tags

# concepts
$minectl new-tags animals clothes countryside drink space \
         fashion food friends plants transport travel

# countries
$minectl new-tags france spain italy usa

# geekery
$minectl new-tags themineproject

###
# set up some implied tags; cats imply animals, motorbikes imply transport, ...

$minectl new-tags cats:animals dogs:animals birds:animals hippos:animals
$minectl new-tags flowers:plants vegetables:plants trees:plants
$minectl new-tags bicycles:transport motorbikes:transport cars:transport

###
# set up tags and implied tags in one go; read from left to right

$minectl new-tags wine:drink beer:drink 
$minectl new-tags white-wine:wine red-wine:wine chardonnay:white-wine rioja:red-wine

###
# for shoe-fetishists "shoes" implies BOTH clothes AND fashion

$minectl new-tags shoes:clothes,fashion

# shoe types

$minectl new-tags \
    mules:shoes \
    pumps:shoes \
    slingbacks:shoes \
    sneakers:shoes \
    stilettos:shoes \
    trainers:shoes

###
# set up some relations

$minectl new-relation alec 1 "Alec Muffett" cats motorbikes drink food themineproject
$minectl new-relation adriana 1 "Adriana Lukas" wine motorbikes themineproject
$minectl new-relation carrie 1 "Carrie Bishop" sneakers trainers themineproject
$minectl new-relation ben 1 "Ben Laurie" wine food motorbikes
$minectl new-relation perry 1 "Perry de Havilland" food drink except:white-wine

##################################################################
##################################################################
##################################################################

exit 0

###
# upload a batch of objects without individual tagging

$minectl upload -s public $SAMPLES/* # wasn't that easy?

###
# highly verbose special cases for tag testing
while read file tags
do
    $minectl upload -s public -t "$tags" $SAMPLES/$file
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
