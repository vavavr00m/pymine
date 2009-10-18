#!/bin/sh

Format() {
    thing=$1
    sattr=$2
    (
    echo "{% if result.$sattr %} <LI>$sattr: {{ result.$sattr }}</LI> {% endif %}"
    ) >> $thing.html
}

for thing in comment item relation tag vurl
do
    (
    echo "{% extends 'base/api.html' %}" 
    echo "{% block api_result %}" 
    echo "<UL>" 
    ) > $thing.html
done

Format comment commentBody
Format comment commentCreated
Format comment commentId
Format comment commentItem
Format comment commentLastModified
Format comment commentRelation
Format comment commentTitle

Format item itemCreated
###Format item itemData
Format item itemDescription
Format item itemFeedLink
Format item itemHasFile
Format item itemHideAfter
Format item itemHideBefore
Format item itemId
Format item itemLastModified
Format item itemName
Format item itemParent
Format item itemSize
Format item itemStatus
Format item itemTags
Format item itemType

Format relation relationCreated
Format relation relationDescription
Format relation relationEmbargoAfter
Format relation relationEmbargoBefore
Format relation relationId
Format relation relationInterests
Format relation relationLastModified
Format relation relationName
Format relation relationNetworkPattern
Format relation relationVersion

Format tag tagCloud
Format tag tagCreated
Format tag tagDescription
Format tag tagId
Format tag tagImplies
Format tag tagLastModified
Format tag tagName

Format vurl vurlAbsoluteUrl
Format vurl vurlCreated
Format vurl vurlId
Format vurl vurlKey
Format vurl vurlLastModified
Format vurl vurlLink
Format vurl vurlName

for thing in comment item relation tag vurl
do
    ( 
	echo "</UL>"  
	echo "{% endblock %}"
    ) >> $thing.html
done
