# Software Requirements #

The goal is to support the latest cut of Django, plus the version previous; when Django moves to 1.2 release, then supported versions will be 1.2 and 1.1 ... and so forth.

At the time of writing (Jan 2010) this means support for Django 1.1 and 1.0 series software; please use the latest versions if possible, and track security bugs and issues closely.

# Software Dependencies #

The dependencies for pymine are approximately:

  1. curl
  1. python-beautifulsoup
  1. python-crypto
  1. python-django
  1. subversion
  1. libapache2-mod-wsgi (if running from Apache in production)

...to use their Ubuntu package names; please mail the project maillist if you're having problems identifying your dependencies.