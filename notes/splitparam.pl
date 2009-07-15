#!/usr/bin/perl

while (<>) {
    die "bad pattern: '$_'\n" unless (m!^([^:]+):\s*(.*)$!o);
    open(FOO, ">$1") || die;
    print FOO $2;
    close(FOO);
}
