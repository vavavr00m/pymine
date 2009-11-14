#!/bin/sh
exec egrep -in "$1" *.py */*.py */*/*.py */*/*/*.py
exit 1
