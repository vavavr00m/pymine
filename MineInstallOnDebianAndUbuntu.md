# Software Pre-requisites and Requirements #

See the MineInstallRequirements page.

# Installation Methods #

## Installation for End-Users ##

First:

  * visit `http://code.google.com/p/pymine/downloads/list`
  * download `http://pymine.googlecode.com/files/pymine_$LATESTVERSION.deb`

Then:

  1. `sudo gdebi pymine_$LATESTVERSION.deb`
  1. `cd /var/mine/pymine`
  1. `sudo sh populate-mine.sh`
  1. `gnome-open http://localhost:9862/`

If you hit a permissions issue:

  * `cd /var/mine/pymine ; make perms`

If you want to see a worked example, there's a Youtube video at

  * http://www.youtube.com/watch?v=v_KIXQqlHwE

## Installation for Django Developers and DIY Web-Admins ##

  1. download http://pymine.googlecode.com/svn/trunk/platform/debian/developer-setup.sh
  1. read the script so you work out what it does
  1. run the script
  1. review the contents of `platform/apache` and `platform/debian` if you want to enable WSGI rather than use the Django development server.