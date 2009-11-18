#!/bin/sh -x

MINE_REPOSITORY="http://pymine.googlecode.com/svn/trunk/"

MINE_PACKAGES="
curl
libapache2-mod-wsgi
python-beautifulsoup
python-crypto
python-django
subversion
"

cd

sudo apt-get install $MINE_PACKAGES

svn checkout $MINE_REPOSITORY pymine

cd pymine

make setup

exec make server

exit 1
