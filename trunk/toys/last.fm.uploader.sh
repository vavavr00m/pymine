#!/bin/sh
url='http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=rj&api_key=b25b959554ed76058ac220b7b2e0a026'
cd
curl "$url" |
awk '
/<track/ {i++}
/<track/,/<\/track/ { f = "last." i ".xml" ; print >> f }
' 
minectl.pl upload -t lastfm last.*.xml
