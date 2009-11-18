#!/bin/sh -x

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

PYMINE_MAINTAINER='Alec Muffett <alec.muffett@gmail.com>'
PYPARENT=var/mine
WORKDIR=/tmp/pydeb$$
USERDIR=`pwd`

##################################################################

test -d $WORKDIR || mkdir -p $WORKDIR || exit 1

cd $WORKDIR || exit 1

mkdir -p debian debian/$PYPARENT debian/DEBIAN debian/usr/share/doc/pymine

chmod -R 755 debian

##################################################################

(
    cd debian/$PYPARENT
    svn checkout http://pymine.googlecode.com/svn/trunk/ pymine
    cd pymine
    make perms
)

PYMINE_VERSION=`cd debian/$PYPARENT/pymine ; svn info | awk '/^Revision:/ {print $2}'`

##################################################################

cat > debian/DEBIAN/control <<EOF
Package: pymine
Version: $PYMINE_VERSION
Section: web
Priority: optional
Architecture: all
Depends: curl, libapache2-mod-wsgi, make, python, python-beautifulsoup, python-crypto, python-django
Maintainer: $PYMINE_MAINTAINER
Description: The Mine Project: Pymine Development Version
 Pymine is a Django/Python tool for implementing a Mine! -
 software which enables personal data sharing via feeds and URLs
 which are different for each subscriber (unlike a traditional blog)
EOF

##################################################################

cat > debian/DEBIAN/prerm <<EOF
#!/bin/sh
set -e
if [ \( "$1" = "upgrade" -o "$1" = "remove" \) -a -L /usr/doc/pymine ]
then
    rm -f /usr/doc/pymine
fi
cd /$PYPARENT/pymine
make clean
EOF

##################################################################

cat > debian/DEBIAN/postinst <<EOF
#!/bin/sh
set -e
if [ "$1" = "configure" ]
then
    if [ -d /usr/doc -a ! -e /usr/doc/pymine -a -d /usr/share/doc/pymine ]; then
	ln -sf ../share/doc/pymine /usr/doc/pymine
    fi
fi
cd /$PYPARENT/pymine
make setup
EOF

##################################################################

(
    cd debian/$PYPARENT/pymine
    svn info
) > debian/usr/share/doc/pymine/changelog

##################################################################

DEBDATE=`date -R`

cat > debian/usr/share/doc/pymine/changelog.Debian <<EOF
pymine ($PYMINE_VERSION) unstable; urgency=low

  * Synced with revision $PYMINE_VERSION of the source

 -- $PYMINE_MAINTAINER  $DEBDATE
EOF

# NB: REQUIRE DOUBLE-SPACE BEFORE DATE ABOVE

##################################################################

grep '^##' debian/$PYPARENT/pymine/NOTICE >> debian/usr/share/doc/pymine/copyright

##################################################################

chmod -R 755 `find debian/DEBIAN -type f`
chmod -R 644 `find debian/usr/share/doc/pymine -type f`
gzip --best debian/usr/share/doc/pymine/changelog*

##################################################################

(
    cd debian/$PYPARENT/pymine
    rm -rf `find . -name .svn`
)

##################################################################

perl -pi~ -e 's/^DEBUG\s*=\s*True/DEBUG = False/o' debian/$PYPARENT/pymine/settings.py.tmpl

##################################################################

sudo chown -R root:root debian
sudo chown -R www-data debian/$PYPARENT/pymine/database
sudo dpkg-deb --build debian || exit 1

DATESTAMP=`date "+%Y%m%d%H%M%S"`

mv debian.deb $USERDIR/pymine_${PYMINE_VERSION}_${DATESTAMP}.deb

##################################################################

exit 0
