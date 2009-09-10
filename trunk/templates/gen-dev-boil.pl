#!/usr/bin/perl
##
## Copyright 2008 Adriana Lukas & Alec Muffett
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

$emphasis = 'em';

##################################################################
print $header;

# body
while (<DATA>) {
    next if /^\s*(\#.*)?$/o;    # ski blanks
    chop;

    ($cmd, @rest) = split;

    if ($cmd eq ':') {          # start block / header
	$anchor = "@rest";
	$anchor =~ s!\W+!!go;
	print "<A NAME=\"$anchor\" HREF=\"#$anchor\">@rest</a>\n";
	print "<UL>\n";
    }
    elsif ($cmd eq '-') {       # end block
	print "</UL>\n";
    }
    elsif ($cmd eq '{') {       # start manual LI
	print "<LI>\n";
	print "<$emphasis>@rest:</$emphasis>\n";
    }
    elsif ($cmd eq '}') {       # end manual LI
	print "</LI>\n";
    }
    elsif ($cmd eq '+') {       # manual text
	$url = shift(@rest);
	push(@rest, $url) if ($#rest < 0);
	print "<A HREF=\"$url\"><button>@rest</button></A>\n";
    }
    elsif ($cmd eq '.') {       # automatic LI
	$url = shift(@rest);
	push(@rest, $url) if ($#rest < 0);
	print "<LI><A HREF=\"$url\">@rest</A></LI>\n";
    }
    elsif ($cmd eq '\'') {      # verbatim quote
	print "@rest <p/>\n";
    }
}

exit 0;
##################################################################
__END__;

' <hr/>
' developer boilerplate

: list existing things
. /ui/list-items.html list items
. /ui/list-relations.html list relations
. /ui/list-tags.html list tags
. /ui/list-vurls.html list vurls
. /ui/list-comments/0.html list comments on all items
. /ui/list-comments/1.html list comments on item 1
. /ui/version.html version
. /admin/ DJANGO ADMIN BACKDOOR
-

: create new things
. /ui/create-comment/1.html create-comment on item 1
. /ui/create-item.html create-item
. /ui/create-relation.html create-relation
. /ui/create-tag.html create-tag
. /ui/create-vurl.html create-vurl
-

: roots
. / mine root
. /api mine api root
. /doc mine doc root
. /get mine get root
. /pub mine pub root
. /archive mine archive root
. /ui mine ui root
-

: testing
. /ui/delete-comment/1.html delete-comment 1
. /ui/read-comment/1.html read-comment 1
. /ui/update-comment/1.html update-comment 1
'
. /ui/delete-item/1.html delete-item 1
. /ui/read-item/1.html read-item 1
. /ui/update-item/1.html update-item 1
'
. /ui/delete-relation/1.html delete-relation 1
. /ui/read-relation/1.html read-relation 1
. /ui/update-relation/1.html update-relation 1
'
. /ui/delete-tag/1.html delete-tag 1
. /ui/read-tag/1.html read-tag 1
. /ui/update-tag/1.html update-tag 1
'
. /ui/delete-vurl/1.html delete-vurl 1
. /ui/read-vurl/1.html read-vurl 1
. /ui/update-vurl/1.html update-vurl 1
-

: mine documentation
. /doc/ local
. #themineproject project documentation
-

: the mine! project
. http://themineproject.org/index.php/about/ about
. http://themineproject.org/ home page and blog
. http://themineproject.org/index.php/feed/ rss feed (full)
. http://themineproject.org/index.php/the-mine-papers/ mine! concepts
-

: pymine software
. http://code.google.com/p/pymine/ google code home page
. http://code.google.com/p/pymine/w/list documentation wiki
. http://code.google.com/p/pymine/updates/list updates and history
. http://code.google.com/p/pymine/issues/list bugs and bug reporting
. http://code.google.com/p/pymine/source/checkout subversion code download
-

: mine! authors
. http://www.mediainfluencer.net/ adriana lukas, mine! inventor
. http://www.crypticide.com/dropsafe/ alec muffett, programmer / geek
-

' &copy; 2008-2009 Adriana Lukas &amp; Alec Muffett;
' pymine is open source software distributed under the Apache 2.0 license,
' please see the <A HREF="http://code.google.com/p/pymine/w/list">project home page</A> for details
' <hr/>
