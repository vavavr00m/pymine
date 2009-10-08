#!/bin/sh
set -x
MC="./minectl.pl -e"
exec 2>&1
$MC new-tags a || exit 1
$MC new-tags b:a || exit 1
$MC new-tags c:a || exit 1
$MC new-tags d:b || exit 1
$MC new-tags e:b,c || exit 1
$MC new-tags f:c || exit 1
$MC new-tags g:d || exit 1
$MC new-tags h:e || exit 1
$MC new-tags i:f || exit 1
$MC update-tag 1 tagImplies="g h" # update a || exit 1
$MC update-tag 5 tagImplies="" # disconnect e || exit 1
