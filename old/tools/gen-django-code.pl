#!/usr/bin/perl

$indent = "    ";
$root_path_strip = "/(api|ui|ie|get|r|v)";

# $value text in <anglebrackets> must be same as lcase($key)
%regexp_lookup = (
    'IID',      '?P<iid>\d+', # iid may be '0' sometimes
    'TID',      '?P<tid>[1-9]\d*',
    'RID',      '?P<rid>[1-9]\d*',
    'RVSN',     '?P<rvsn>[1-9]\d*',
    'CID',      '?P<cid>[1-9]\d*',
    'VID',      '?P<vid>[1-9]\d*',
    'FMT',      '?P<fmt>(rdr|xml|json|raw)',
    'VURLKEY',  '?P<vurlkey>[-_A-Za-z0-9]+',
    'SATTR',    '?P<sattr>(__)?[A-Za-z][_A-Za-z]*',  #  f,  foo,  fooBar,  __fooBar
    'RATTR',    '?P<rattr>[A-Za-z][_A-Za-z]*',       #  f,  foo,  fooBar
    'MINEKEY',  '?P<minekey>[-_A-Za-z0-9]+=*',
    'EFMT',     '?P<efmt>(zip|tar)',
    'SUFFIX',   '?P<suffix>.+',
    'TRASH',    '.*',
    );


while (<DATA>) {
    next if (/^\s*(\#.*)?$/o);        # skip comments and blank lines

    s/#.*$//go;                       # trim trailing comments

    ($class, $http_method, $url, $pymethod) = split;

    $output = \@{$text{'views'}{$class}};

    $template_prefix = $pymethod;

    $template_prefix =~ s!-!/!go;

    $pymethod =~ tr!-!_!;

    $callback = "$class.$pymethod";

    $pattern = $url;

    $pattern =~ s!\.!\\.!go; # escape all dots

    $pattern =~ s/([A-Z]+)/"(" . ($regexp_lookup{$1}||"&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& $1 &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&") . ")"/goe;

    @kwds = grep(/^[A-Z]+$/o, split(/\b/o, $url));

    @kwds = map { lc($_) } grep(!/^(FMT|TRASH)$/o, @kwds); # exclude .FMT/TRASH which is handled elsewhere/ignored

    $aaa = join(", ", 'request', @kwds, '*args', '**kwargs');
    $aaa2 = join(", ", @kwds);

    push(@{$output}, "## rest: $http_method $url\n");
    push(@{$output}, "## function: $pymethod\n");
    push(@{$output}, "## declared args: @kwds\n");
    push(@{$output}, "def $pymethod($aaa):\n$indent\"\"\"$pymethod($aaa2) returns ...\"\"\"\n");

    push(@{$output}, "${indent}# TBD: DELETE THIS COMMENT WHEN THE CODE IS DONE\n");

    if (($class eq 'api') and ($url ne '/api')) { # root
	push(@{$output}, "${indent}return { 'status': 'not yet implemented' }\n");
    }
    else {
	push(@{$output}, "${indent}s = api.$pymethod($aaa)\n");
	push(@{$output}, "${indent}return render_to_response('$template_prefix.html', s)\n");
    }

    push(@{$output}, "\n");

    push(@{$patterns{$pattern}}, "'$http_method': $callback");

    $class_of{$pattern} = $class;

}

##################################################################

foreach $pattern (sort {$b cmp $a} keys %patterns) {

    $class = $class_of{$pattern};

    $output = \@{$text{'urls'}{$class}};

    $foo = join(",\n$indent  ", @{$patterns{$pattern}});

    if (($class eq 'api') && ($pattern =~ /fmt/)) {
	$dispatch = "API_CALL";
    }
    elsif ($class eq 'get') {
	$dispatch = "REST_NOAUTH";
    }
    else {
	$dispatch = "REST";
    }

    $dispatch = "REST" if ($pattern eq ''); # root

    $pattern =~ s!^$root_path_strip!!o;
    $pattern =~ s!^/!!o;

    push(@{$output}, $indent, "(r'^$pattern\$',\n$indent $dispatch, { $foo }),\n");
}


##################################################################

@foo = keys %text;

foreach $file (sort keys %text) {

    foreach $class (sort keys %{ $text{$file}}) {
	open(FOO, ">tmp.$class.$file.py");
	print FOO @{$text{$file}{$class}};
	close(FOO);
    }
}

##################################################################
##################################################################
##################################################################
__END__;

mine   GET    /                              root-mine
mine   GET    /favicon.ico                   root-favicon
#mine   GET    /pub/                          root-pub
#mine   GET    /pub/SUFFIX                    handle-pub

get    GET    /get/MINEKEY(/TRASH)?          read-minekey
get    POST   /get/MINEKEY(/TRASH)?          submit-minekey
get    POST   /get/m                         field-minekey # accept POST for any minekey
get    GET    /get/i/VID                     redirect-vid # short to long remapping
get    GET    /get/k/VURLKEY                 redirect-vurlkey # short to long remapping
get    GET    /get/n/SUFFIX                  redirect-vurlname # long to long remapping

api    DELETE /api/comment/CID.FMT           delete-comment
api    GET    /api/comment/CID.FMT           read-comment
api    POST   /api/comment/CID.FMT           update-comment
api    DELETE /api/comment/CID/SATTR.FMT     delete-comment-key
api    GET    /api/comment/CID/SATTR.FMT     get-comment-key
api    POST   /api/comment/item/IID.FMT      create-comment # IID==0 -> comment on entire feed
api    GET    /api/comment/item/IID.FMT      list-comments # IID==0 -> list all comments

api    GET    /api/ie/export.EFMT            export-mine
api    GET    /api/ie/import.EFMT            import-mine

api    POST   /api/item.FMT                  create-item
api    GET    /api/item.FMT                  list-items
api    GET    /api/item/IID                  read-item-data # this is the raw item method
api    DELETE /api/item/IID.FMT              delete-item
api    GET    /api/item/IID.FMT              read-item
api    POST   /api/item/IID.FMT              update-item
api    DELETE /api/item/IID/SATTR.FMT        delete-item-key
api    GET    /api/item/IID/SATTR.FMT        get-item-key

api    GET    /api/registry.FMT              list-registry
api    POST   /api/registry/RATTR.FMT        amend-registry-key
api    DELETE /api/registry/RATTR.FMT        delete-registry-key
api    GET    /api/registry/RATTR.FMT        get-registry-key

api    POST   /api/relation.FMT              create-relation
api    GET    /api/relation.FMT              list-relations
api    DELETE /api/relation/RID.FMT          delete-relation
api    GET    /api/relation/RID.FMT          read-relation
api    POST   /api/relation/RID.FMT          update-relation
api    DELETE /api/relation/RID/SATTR.FMT    delete-relation-key
api    GET    /api/relation/RID/SATTR.FMT    get-relation-key

api    POST   /api/tag.FMT                   create-tag
api    GET    /api/tag.FMT                   list-tags
api    DELETE /api/tag/TID.FMT               delete-tag
api    GET    /api/tag/TID.FMT               read-tag
api    POST   /api/tag/TID.FMT               update-tag
api    DELETE /api/tag/TID/SATTR.FMT         delete-tag-key
api    GET    /api/tag/TID/SATTR.FMT         get-tag-key

api    GET    /api/url/RID.FMT               encode-minekey1
api    GET    /api/url/RID/IID.FMT           encode-minekey2
api    GET    /api/url/RID/RVSN/IID.FMT      encode-minekey3

api    GET    /api/version.FMT               read-version

api    POST   /api/vurl.FMT                  create-vurl
api    GET    /api/vurl.FMT                  list-vurls
api    DELETE /api/vurl/VID.FMT              delete-vurl
api    GET    /api/vurl/VID.FMT              read-vurl
api    POST   /api/vurl/VID.FMT              update-vurl
api    DELETE /api/vurl/VID/SATTR.FMT        delete-vurl-key
api    GET    /api/vurl/VID/SATTR.FMT        get-vurl-key

ui     GET    /ui/create/comment/IID.html    create-comment
ui     GET    /ui/create/item.html           create-item
ui     GET    /ui/create/relation.html       create-relation
ui     GET    /ui/create/tag.html            create-tag
ui     GET    /ui/create/text.html           create-text
ui     GET    /ui/create/vurl.html           create-vurl

ui     GET    /ui/dash/comments.html         dash-comments
ui     GET    /ui/dash/items.html            dash-items
ui     GET    /ui/dash/relations.html        dash-relations
ui     GET    /ui/dash/search.html           dash-search
ui     GET    /ui/dash/settings.html         dash-settings
ui     GET    /ui/dash/tags.html             dash-tags
ui     GET    /ui/dash/vurls.html            dash-vurls

ui     GET    /ui/delete/comment/CID.html    delete-comment
ui     GET    /ui/delete/item/IID.html       delete-item
ui     GET    /ui/delete/relation/RID.html   delete-relation
ui     GET    /ui/delete/tag/TID.html        delete-tag
ui     GET    /ui/delete/vurl/VID.html       delete-vurl

ui     GET    /ui/list/comments/IID.html     list-comments
ui     GET    /ui/list/items.html            list-items
ui     GET    /ui/list/relations.html        list-relations
ui     GET    /ui/list/tags.html             list-tags
ui     GET    /ui/list/vurls.html            list-vurls

ui     GET    /ui/read/comment/CID.html      read-comment
ui     GET    /ui/read/item/IID.html         read-item
ui     GET    /ui/read/relation/RID.html     read-relation
ui     GET    /ui/read/tag/TID.html          read-tag
ui     GET    /ui/read/vurl/VID.html         read-vurl

ui     GET    /ui/search/comments.html       search-comments
ui     GET    /ui/search/items.html          search-items
ui     GET    /ui/search/relations.html      search-relations
ui     GET    /ui/search/tags.html           search-tags
ui     GET    /ui/search/vurls.html          search-vurls

ui     GET    /ui/update/comment/CID.html    update-comment
ui     GET    /ui/update/item/IID.html       update-item
ui     GET    /ui/update/relation/RID.html   update-relation
ui     GET    /ui/update/tag/TID.html        update-tag
ui     GET    /ui/update/vurl/VID.html       update-vurl

ui     GET    /ui/version.html               read-version
