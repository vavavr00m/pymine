#!/bin/sh
exec egrep -in "$1" * */* */*/* */*/*/* */*/*/*/*
exit 1
