#!/bin/sh

FMT() {
    thing=$1
    sattr=$2
    echo "<LI>$sattr: {{ $thing.$sattr }}</LI>" >> read-$thing.html
}

for thing in comment item relation tag vurl
do
    echo "{% for $thing in result %}"  > read-$thing.html
done

FMT comment commentBody
FMT comment commentCreated
FMT comment commentId
FMT comment commentItem
FMT comment commentLastModified
FMT comment commentLikes
FMT comment commentRelation
FMT comment commentTitle

FMT item itemCreated
FMT item itemData
FMT item itemDescription
FMT item itemHideAfter
FMT item itemHideBefore
FMT item itemId
FMT item itemLastModified
FMT item itemName
FMT item itemStatus
FMT item itemTags
FMT item itemType

FMT relation relationCallbackURL
FMT relation relationCreated
FMT relation relationDescription
FMT relation relationEmailAddress
FMT relation relationEmbargoAfter
FMT relation relationEmbargoBefore
FMT relation relationHomepageURL
FMT relation relationId
FMT relation relationImageURL
FMT relation relationInterests
FMT relation relationLastModified
FMT relation relationName
FMT relation relationNetworkPattern
FMT relation relationVersion

FMT tag tagCreated
FMT tag tagDescription
FMT tag tagId
FMT tag tagImplies
FMT tag tagLastModified
FMT tag tagName

FMT vurl vurlCreated
FMT vurl vurlId
FMT vurl vurlLastModified
FMT vurl vurlLink
FMT vurl vurlName
FMT vurl vurlTags

for thing in comment item relation tag vurl
do
    echo "{% endfor %}"  >> read-$thing.html
done
