#!/usr/bin/perl

%regexp_lookup = ( # $value text in <anglebrackets> must be same as lcase($key)
    'CID', '?P<cid>\d+',
    'FMT', '?P<fmt>(xml|json|py|txt)',
    'IID', '?P<iid>\d+',
    'KEY', '?P<key>\w+',
    'RID', '?P<rid>\d+',
    'RVSN', '?P<rvsn>\d+',
    'SUFFIX', '?P<suffix>.+',
    'TID', '?P<tid>\d+',
    );

%rest_lookup = (
    'DUMMY', 'dummy',
    'GET', 'read',
    'POST', 'create',
    'PUT', 'update',
    'DELETE', 'delete',
);

while (<DATA>) {
    if (/^\s*(\#.*)?$/o) {
	# skip comments and blank lines
	push(@view_output, '#' x 66);
	push(@view_output, "\n");
	push(@view_output, "\n");
	next;
    }

    ($url, $http_method, $suffix) = split;

    $suffix =~ tr!-!_!;
    $pymethod = $rest_lookup{$http_method} . "_" . $suffix;

    if ($url =~ m!/api/!o) {
	$module = "api";
    }
    elsif ($url =~ m!/ui/!o) {
	$module = "ui";
    }
    else {
	$module = "mine";
    }

    $callback = "$module.$pymethod";

    $pattern = $url;
    $pattern =~ s/([A-Z]+)/"(" . ($regexp_lookup{$1}||"--------$1--------") . ")"/goe;

    @kwds = grep(/^[A-Z]+$/o, split(/\b/o, $url));
    @kwds = map { lc($_) } grep(!/^(FMT)$/o, @kwds);
    $aaa = join(", ", 'request', @kwds, '*args', '**kwargs');

    push(@view_output, "## url: $url\n");
    push(@view_output, "## method: $pymethod\n");
    push(@view_output, "## args: @kwds\n");
    push(@view_output, "def $pymethod($aaa):\n");

    if ($url =~ m!^api/.!o) {
	push(@view_output, "    return { 'status': 'not yet implemented' }\n");
    } 
    else {
	push(@view_output, "    raise Http404('method $pymethod for url $url is not yet implemented')\n");
    }

    push(@view_output, "\n");

    push(@{$patterns{$pattern}}, "'$http_method': $callback");

}

print @view_output;

print "#" x 66, "\n\n";

$indent = "    ";

foreach $pattern (sort keys %patterns) {
    $foo = join(", ", @{$patterns{$pattern}});

    if ($pattern =~ m!/api/!o) {
	$dispatch = "api.DISPATCH";
    }
    elsif ($pattern =~ m!/ui/!o) {
	$dispatch = "ui.RESPOND";
    }
    else {
	$dispatch = "mine.REST";
    }

    print $indent, "(r'^$pattern\$',\n$indent $dispatch, {$foo}),\n";
}

__END__;
/                                GET     mine-root
/api                             GET     api-root
/doc                             GET     doc
/get                             GET     minekey
/get                             POST    minekey
/pub                             GET     pub
/ui                              GET     ui-root

/api/config.FMT                  GET     config
/api/config.FMT                  POST    config
/api/item.FMT                    GET     item-list
/api/item.FMT                    POST    item
/api/item/IID                    GET     item-data
/api/item/IID                    POST    item-data
/api/item/IID.FMT                DELETE  item
/api/item/IID.FMT                GET     item
/api/item/IID/CID.FMT            DELETE  comment
/api/item/IID/CID.FMT            GET     comment
/api/item/IID/CID/key.FMT        POST    comment-key
/api/item/IID/CID/key/KEY.FMT    DELETE  comment-key
/api/item/IID/CID/key/KEY.FMT    GET     comment-key
/api/item/IID/CID/key/KEY.FMT    POST    comment-key
/api/item/IID/clone.FMT          GET     clone-list
/api/item/IID/clone.FMT          POST    clone
/api/item/IID/comment.FMT        GET     comment-list
/api/item/IID/comment.FMT        POST    comment
/api/item/IID/key.FMT            POST    item-key
/api/item/IID/key/KEY.FMT        DELETE  item-key
/api/item/IID/key/KEY.FMT        GET     item-key
/api/item/IID/key/KEY.FMT        POST    item-key
/api/relation.FMT                GET     relation-list
/api/relation.FMT                POST    relation
/api/relation/RID.FMT            DELETE  relation
/api/relation/RID.FMT            GET     relation
/api/relation/RID/key.FMT        POST    relation-key
/api/relation/RID/key/KEY.FMT    DELETE  relation-key
/api/relation/RID/key/KEY.FMT    GET     relation-key
/api/relation/RID/key/KEY.FMT    POST    relation-key
/api/select/item.FMT             GET     select-item
/api/select/relation.FMT         GET     select-relation
/api/select/tag.FMT              GET     select-tag
/api/tag.FMT                     GET     tag-list
/api/tag.FMT                     POST    tag
/api/tag/TID.FMT                 DELETE  tag
/api/tag/TID.FMT                 GET     tag
/api/tag/TID/key.FMT             POST    tag-key
/api/tag/TID/key/KEY.FMT         DELETE  tag-key
/api/tag/TID/key/KEY.FMT         GET     tag-key
/api/tag/TID/key/KEY.FMT         POST    tag-key
/api/url/RID.FMT                 GET     encode-minekey
/api/url/RID/IID.FMT             GET     encode-minekey
/api/url/RID/RVSN/IID.FMT        GET     encode-minekey
/api/version.FMT                 GET     version

/ui/create-comment/IID.html      GET     create-comment
/ui/create-item.html             GET     create-item
/ui/create-relation.html         GET     create-relation
/ui/create-tag.html              GET     create-tag
/ui/data/IID                     GET     data/IID
/ui/delete-comment/IID/CID.html  GET     delete-comment
/ui/delete-item/IID.html         GET     delete-item
/ui/delete-relation/RID.html     GET     delete-relation
/ui/delete-tag/TID.html          GET     delete-tag
/ui/list-comments/IID.html       GET     list-comments
/ui/list-items.html              GET     list-items
/ui/list-relations.html          GET     list-relations
/ui/list-tags.html               GET     list-tags
/ui/read-comment/IID/CID.html    GET     read-comment
/ui/read-config.html             GET     read-config
/ui/read-item/IID.html           GET     read-item
/ui/read-relation/RID.html       GET     read-relation
/ui/read-tag/TID.html            GET     read-tag
/ui/update-comment/IID/CID.html  GET     update-comment
/ui/update-config.html           GET     update-config
/ui/update-item/IID.html         GET     update-item
/ui/update-relation/RID.html     GET     update-relation
/ui/update-tag/TID.html          GET     update-tag
/ui/version.html                 GET     version.html
