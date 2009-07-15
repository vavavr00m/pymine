#!/bin/sh

while read file
do
    mv $file $file.f

    test -d $file || mkdir $file || exit 1

    if [ -f $file.data ]
    then
	mv $file.data $file/data || exit 1
    fi

    (
	cd $file
	suffix=`basename $file`
	/Users/alecm/protomine/pymine/database/splitparam.pl < ../$suffix.f
    )
done
