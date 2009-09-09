#!/bin/sh

for i in urls.py */urls.py views.py */views.py
do
    me $i
done
