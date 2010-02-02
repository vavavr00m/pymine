#!/bin/sh -x

# kludge of the week
for i in comment item feed tag vurl
do
    sed -e s/result/hash/g < action-$i.html > action2-$i.html
done
