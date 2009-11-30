#!/bin/sh
# horrible kludge but it saves typing
parent=`(cd .. ; pwd)`
PYTHONPATH=$PYTHONPATH:$parent
export PYTHONPATH
DJANGO_SETTINGS_MODULE=pymine.settings
export DJANGO_SETTINGS_MODULE
exec "$@"
exit 1
