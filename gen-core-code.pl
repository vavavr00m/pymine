#!/usr/bin/perl
##
## Copyright 2010 Adriana Lukas & Alec Muffett
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

# MODULES / NAMESPACES / DJANGO APPLICATIONS
# api:  REST api calls and model
# mine: root of app
# ui:   user interface

# ATTRIBUTES
# feedFoo: a feed attribute
# itemFoo: a item attribute
# $itemFoo: a item extended attribute
# __foo__: an attribute that may not be retreived except over SSL or via django admin interface
# $__foo__: an extended attribute that may not be retreived except over SSL or via django admin interface

# don't mess with the expressions too much; the idea is to be very
# (but not insanely) strict about what you will accept, thereby
# reducing exposure to stupidity and hacking.

# there must be one and only one ID or IDZ per url pattern; the REST
# space has been designed cleanly to ensure this is always the case;
# the only notable oddity are the small selection of comment-related
# url-patterns which take a target itemId infix.  Where this is not
# possible (ie: the minekey elements) instead we create entire
# surrogates.

# the regexp /[1-9]\d*/ represents "integer > zero", hence ID

# the regexp /\d+/ represents "integer >= zero", hence IDZ

%expressions =
    (
     # minekey elements
     #(MK_HMAC)/(MK_FID)/(MK_FVERSION)/(MK_IID)/(MK_DEPTH)/(MK_TYPE).(MK_EXT)
     'MK_HMAC', '?P<mk_hmac>[-\w]{43}*',
     'MK_FID', '?P<mk_fid>[1-9]\d*',
     'MK_FVERSION', '?P<mk_fversion>[1-9]\d*',
     'MK_IID', '?P<mk_iid>\d+',
     'MK_DEPTH', '?P<mk_depth>[1-9]\d*',
     'MK_TYPE', '?P<mk_type>(data|icon|submit)',
     'MK_EXT', '?P<mk_ext>\w+',

     # various forms of thing-ids, zero not permitted
     'ID', '?P<id>[1-9]\d*',

     # ditto, but where id==0 is permitted
     'IDZ', '?P<idz>\d+',

     # acceptable output formats
     'FMT', '?P<fmt>(json|xml|txt|rdr)',

     # base58-encoded id
     'VURLKEY', '?P<vurlkey>[-\w]+',

     # registry attribute name, must start with letter/underscore
     'RATTR', '?P<rattr>[_A-Za-z]\w*',

     # structure attribute name, ditto with optional '$' prefix for Xattrs
     'ATTR', '?P<sattr>\$?[_A-Za-z]\w*',

     # token: a plausible, safe dummy filename
     'TOKEN', '?P<token>[\-\.\w]*',

     # suffix: swallow the rest of the string
     'SUFFIX', '?P<suffix>.*',
    );

$indent = "    ";

while (<DATA>) {
    next if (/^\s*(\#.*)?$/o);        # skip comments and blank lines
    s/#.*$//go;                       # trim trailing comments

    ($module, $method, $url, $pydoc, @args) = split;

    $pyfunc = $pydoc;
    $pyfunc =~ s/-/_/go;

    $viewsref = \@{$output{'views'}{$module}};
    $urlsref =  \@{$output{'urls'}{$module}};

    $pattern = $url;
    $pattern =~ s!\.!\\.!go; # escape all dots
    $pattern =~ s/([_A-Z]+)/ ($expressions{$1} || "----> $1 <----") /goe;

    @kwds = grep(/^[_A-Z]+$/o, split(/\b/o, $url));
    @kwds = map { lc($_) } grep(!/^(FMT)$/o, @kwds);

    @vargs = map { (split(":"))[0] } @args;
    @uargs = map { (split(":"))[1] } @args;

    #$src = join(", ", 'request', @vargs, @kwds, '*args', '**kwargs');
    $src = join(", ", 'request', @vargs, @kwds, '**kwargs');
    $dst = $defargs{$module}{$pyfunc};

    if ($dst eq '') {
	$defargs{$module}{$pyfunc} = $src;
    }
    elsif ($src ne $dst) {
	warn "check signature: ($module $url $pyfunc)\n$src\n$dst\n\n";
    }

    push(@{ $implements{$module}{$pyfunc} }, "$method $url");

    $urldispatch{$module}{$pattern}{$method} = join(", ", "$module.$pyfunc",  @uargs);
}

sub print_boilerplate {
    my $module = shift;

    if ($module eq 'api') {
	print $indent, "s = {}\n";
	print $indent, "return Envelope(request, s)\n";
    }
    elsif ($module eq 'ui' or $module eq 'dev') {
	print $indent, "s = {}\n";
	print $indent, "return render_to_response(template, s)\n";
    }
    else {
	print $indent, "pass\n";
    }
}

foreach $module (sort keys %defargs) {
    open(F, ">tmp.$module.views.py") || die "open: $!\n";
    select(F);
    foreach $pyfunc (sort keys %{ $defargs{$module} }) {
	print "#"x66, "\n";
	print "\n";
	print "# this definition ($pyfunc) is auto-generated.\n";
	print "# ensure that any changes are made via the generator.\n";
	$a = $defargs{$module}{$pyfunc};
	print "def $pyfunc($a):\n";
	print $indent, '"""', "\n";
	print $indent, "arguments: $a\n";
	foreach $i (@{ $implements{$module}{$pyfunc} }) {
	    print $indent, "implements: $i\n";
	}
	print $indent, "returns: ...\n";
	print $indent, '"""', "\n";
	&print_boilerplate($module);
	print "\n";
    }
    print "#"x66, "\n";
    select(STDOUT);
}

foreach $module (sort keys %urldispatch) {
    open(F, ">tmp.$module.urls.py") || die "open: $!\n";
    select(F);
    print "#"x66, "\n";
    print "# this code is auto-generated.\n";
    print "# ensure that any changes are made via the generator.\n";
    print "\n";
    print "urlpatterns += patterns('',\n";
    foreach $pattern (sort keys %{ $urldispatch{$module} }) {
	$p = $pattern;
	$p =~ s!^/($module/)?!!; # remove the leading '/api' or '/ui' IFF it matches $module

	if ($module eq "api") {
	    if ($pattern =~ /\<fmt\>/) {
		$wrapper = 'API_REST';
	    }
	    else {
		$wrapper = 'HTTP_METHOD';
	    }
	}
	elsif ($pattern =~ m!^/(favicon|key|page|pub|vurl)\b!) {
	    $wrapper = 'HTTP_METHOD_NOAUTH';
	}
	else {
	    $wrapper = 'HTTP_METHOD';
	}

	print $indent, "(", "r'^$p\$',\n$indent $wrapper, { ";

	@methods = sort keys %{ $urldispatch{$module}{$pattern} };

	foreach $method (@methods) {
	    $x = $urldispatch{$module}{$pattern}{$method};
	    print "'$method' : [ $x ],";
	    
	    if ($method ne $methods[-1]) {
		print "\n$indent";
	    }
	    else {
		print " ";
	    }
	}
	print "}),\n";

    }
    print $indent, ")\n\n";
    print "#"x66, "\n";
    select(STDOUT);
}

##################################################################
##################################################################
##################################################################
__END__;

# Ok, this is the code to generate most of the mine django
# boilerplate; the syntax is pretty simple:

# field 1: the module we're working on

# field 2: the relevant HTTP method for the subsequent URL

# field 3: the URL for the REST method or whatever; dots are escaped,
# parenthesised subexpressions in CAPITAL_LETTERS are looked-up in the
# table of regular expressions above and substituted.

# field 4: the hyphenated-pseudo-name for the API routine we're
# calling, fit for documentation purposes; this is coersced into
# underscores and used as a function name in the actual boilerplate
# code.

# all remaining fields should be of "foo:bar" syntax, where:

# foo = the formal parameter name to be used in the 'views' template

# bar = the hardcoded formal parameter value to be passed from the
# 'urls' invocation, setting the 'foo' parameter above

# The code checks the signatures of all permutations of HTTPmethod vs
# URL and ensures that there are balanced numbers of arguments in the
# urls and views templates

# ps: note to alec: | cts -k 3

##################################################################

api  GET     /api/data/(ID)(/TOKEN)          read-item-data
api  GET     /api/icon/(ID)(/TOKEN)          read-item-icon
api  POST    /api/encode.(FMT)               encode-minekey
api  GET     /api/version.(FMT)              read-version

api  GET     /api/registry.(FMT)             list-registry
api  DELETE  /api/registry/(RATTR).(FMT)     delete-registry-attr
api  GET     /api/registry/(RATTR).(FMT)     get-registry-attr
api  POST    /api/registry/(RATTR).(FMT)     update-registry-attr

api  POST    /api/comment/item/(IDZ).(FMT)   create-comment        #special
api  GET     /api/comment/item/(IDZ).(FMT)   list-comments         #special
api  DELETE  /api/comment/(ID).(FMT)         delete-thing          thyng:Comment
api  GET     /api/comment/(ID).(FMT)         read-thing            thyng:Comment
api  POST    /api/comment/(ID).(FMT)         update-thing          thyng:Comment
api  DELETE  /api/comment/(ID)/(ATTR).(FMT)  delete-thing-attr     thyng:Comment
api  GET     /api/comment/(ID)/(ATTR).(FMT)  get-thing-attr        thyng:Comment

api  POST    /api/feed.(FMT)                 create-thing          thyng:Feed
api  GET     /api/feed.(FMT)                 list-things           thyng:Feed
api  DELETE  /api/feed/(ID).(FMT)            delete-thing          thyng:Feed
api  GET     /api/feed/(ID).(FMT)            read-thing            thyng:Feed
api  POST    /api/feed/(ID).(FMT)            update-thing          thyng:Feed
api  DELETE  /api/feed/(ID)/(ATTR).(FMT)     delete-thing-attr     thyng:Feed
api  GET     /api/feed/(ID)/(ATTR).(FMT)     get-thing-attr        thyng:Feed

api  POST    /api/item.(FMT)                 create-thing          thyng:Item
api  GET     /api/item.(FMT)                 list-things           thyng:Item
api  DELETE  /api/item/(ID).(FMT)            delete-thing          thyng:Item
api  GET     /api/item/(ID).(FMT)            read-thing            thyng:Item
api  POST    /api/item/(ID).(FMT)            update-thing          thyng:Item
api  DELETE  /api/item/(ID)/(ATTR).(FMT)     delete-thing-attr     thyng:Item
api  GET     /api/item/(ID)/(ATTR).(FMT)     get-thing-attr        thyng:Item

api  GET     /api/query/comment.(FMT)        query-thing           thyng:Comment
api  GET     /api/query/feed.(FMT)           query-thing           thyng:Feed
api  GET     /api/query/item.(FMT)           query-thing           thyng:Item
api  GET     /api/query/tag.(FMT)            query-thing           thyng:Tag
api  GET     /api/query/vurl.(FMT)           query-thing           thyng:Vurl

api  POST    /api/tag.(FMT)                  create-thing          thyng:Tag
api  GET     /api/tag.(FMT)                  list-things           thyng:Tag
api  DELETE  /api/tag/(ID).(FMT)             delete-thing          thyng:Tag
api  GET     /api/tag/(ID).(FMT)             read-thing            thyng:Tag
api  POST    /api/tag/(ID).(FMT)             update-thing          thyng:Tag
api  DELETE  /api/tag/(ID)/(ATTR).(FMT)      delete-thing-attr     thyng:Tag
api  GET     /api/tag/(ID)/(ATTR).(FMT)      get-thing-attr        thyng:Tag

api  POST    /api/vurl.(FMT)                 create-thing          thyng:Vurl
api  GET     /api/vurl.(FMT)                 list-things           thyng:Vurl
api  DELETE  /api/vurl/(ID).(FMT)            delete-thing          thyng:Vurl
api  GET     /api/vurl/(ID).(FMT)            read-thing            thyng:Vurl
api  POST    /api/vurl/(ID).(FMT)            update-thing          thyng:Vurl
api  DELETE  /api/vurl/(ID)/(ATTR).(FMT)     delete-thing-attr     thyng:Vurl
api  GET     /api/vurl/(ID)/(ATTR).(FMT)     get-thing-attr        thyng:Vurl

##################################################################

mine  POST  /key/(MK_HMAC)/(MK_FID)/(MK_FVERSION)/(MK_IID)/(MK_DEPTH)/(MK_TYPE).(MK_EXT)  minekey-submit
mine  GET   /key/(MK_HMAC)/(MK_FID)/(MK_FVERSION)/(MK_IID)/(MK_DEPTH)/(MK_TYPE).(MK_EXT)  minekey-read

##################################################################

mine  GET  /                mine-redirect      target:'ui/dash/home.html'
mine  GET  /favicon.ico     get-favicon
mine  GET  /page/(SUFFIX)   vurl-read-by-name
mine  GET  /pub(/SUFFIX)    mine-public
mine  GET  /vurl/(VURLKEY)  vurl-read-by-key

##################################################################

ui  GET  /ui/create/comment/(IDZ).html  create-comment     template:'create/comment.html'
ui  GET  /ui/create/feed.html           render             template:'create/feed.html'
ui  GET  /ui/create/item.html           render             template:'create/item.html'
ui  GET  /ui/create/tag.html            render             template:'create/tag.html'
ui  GET  /ui/create/vurl.html           render             template:'create/vurl.html'
ui  GET  /ui/dash/comments.html         dash-comments      template:'dash/comments.html'
ui  GET  /ui/dash/feeds.html            dash-feeds         template:'dash/feeds.html'
ui  GET  /ui/dash/home.html             render             template:'dash/home.html'
ui  GET  /ui/dash/items.html            dash-items         template:'dash/items.html'
ui  GET  /ui/dash/search.html           render             template:'dash/search.html'
ui  GET  /ui/dash/settings.html         render             template:'dash/settings.html'
ui  GET  /ui/dash/tags.html             dash-tags          template:'dash/tags.html'
ui  GET  /ui/dash/vurls.html            dash-vurls         template:'dash/vurls.html'
ui  GET  /ui/delete/comment/(ID).html   delete-comment     template:'delete/comment.html'
ui  GET  /ui/delete/feed/(ID).html      delete-feed        template:'delete/feed.html'
ui  GET  /ui/delete/item/(ID).html      delete-item        template:'delete/item.html'
ui  GET  /ui/delete/tag/(ID).html       delete-tag         template:'delete/tag.html'
ui  GET  /ui/delete/vurl/(ID).html      delete-vurl        template:'delete/vurl.html'
ui  GET  /ui/list/comments/(IDZ).html   list-comments      template:'list/comments.html'
ui  GET  /ui/list/feeds.html            list-feeds         template:'list/feeds.html'
ui  GET  /ui/list/items.html            list-items         template:'list/items.html'
ui  GET  /ui/list/tags.html             list-tags          template:'list/tags.html'
ui  GET  /ui/list/vurls.html            list-vurls         template:'list/vurls.html'
ui  GET  /ui/read/comment/(ID).html     read-comment       template:'read/comment.html'
ui  GET  /ui/read/feed/(ID).html        read-feed          template:'read/feed.html'
ui  GET  /ui/read/item/(ID).html        read-item          template:'read/item.html'
ui  GET  /ui/read/tag/(ID).html         read-tag           template:'read/tag.html'
ui  GET  /ui/read/vurl/(ID).html        read-vurl          template:'read/vurl.html'
ui  GET  /ui/search/comments.html       search-comments    template:'search/comments.html'
ui  GET  /ui/search/feeds.html          search-feeds       template:'search/feeds.html'
ui  GET  /ui/search/items.html          search-items       template:'search/items.html'
ui  GET  /ui/search/tags.html           search-tags        template:'search/tags.html'
ui  GET  /ui/search/vurls.html          search-vurls       template:'search/vurls.html'
ui  GET  /ui/update/comment/(ID).html   update-comment     template:'update/comment.html'
ui  GET  /ui/update/feed/(ID).html      update-feed        template:'update/feed.html'
ui  GET  /ui/update/item/(ID).html      update-item        template:'update/item.html'
ui  GET  /ui/update/tag/(ID).html       update-tag         template:'update/tag.html'
ui  GET  /ui/update/vurl/(ID).html      update-vurl        template:'update/vurl.html'
ui  GET  /ui/version.html               version            template:'version.html'

##################################################################

dev  GET  /dev/home.html  render  template:'dev/tbd.html'
