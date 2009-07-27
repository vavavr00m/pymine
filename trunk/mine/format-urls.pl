#!/usr/bin/perl

%regexp_lookup = ( # $value text in <anglebrackets> must be same as lcase($key)
    'CID', '?P<cid>\d+',
    'FMT', '?P<fmt>(xml|json|html|txt)',
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

$module = "views";

while (<DATA>) {
    next if /^\s*(\#.*)?$/o;	# skip comments and blank lines

    ($url, $http_method, $suffix) = split;

    $suffix =~ tr!-!_!;

    $pymethod = $rest_lookup{$http_method} . "_" . $suffix;
    $callback = "$module.$pymethod";

    $pattern = $url;
    $pattern =~ s/([A-Z]+)/"(" . ($regexp_lookup{$1}||"--------$1--------") . ")"/goe;

    @kwds = grep(/^[A-Z]+$/o, split(/\b/o, $url));
    @kwds = map { lc($_) } grep(!/^(FMT)$/o, @kwds);
    $aaa = join(", ", 'request', @kwds, '*args', '**kwargs');

    push(@view_output, "#### method: $pymethod url: $url\n");
    push(@view_output, "def $pymethod($aaa):\n");
    push(@view_output, "    raise Http404('method $pymethod for url $url is not yet implemented')\n");
    push(@view_output, "\n");

    push(@{$patterns{$pattern}}, "'$http_method': $callback");

}

print @view_output;

print "-" x 66, "\n";

foreach $pattern (sort keys %patterns) {
    $foo = join(", ", @{$patterns{$pattern}});
    print "    ", "(r'^$pattern\$', views.rest, {$foo}),\n";
}

__END__;
#api/config.FMT                GET     config
#api/config.FMT                POST    config
#api/item.FMT                  GET     item_list
#api/item.FMT                  POST    item
#api/item/IID                  GET     item_data
#api/item/IID                  PUT     item_data
#api/item/IID.FMT              DELETE  item
#api/item/IID.FMT              GET     item
#api/item/IID/CID.FMT          DELETE  comment
#api/item/IID/CID.FMT          GET     comment
#api/item/IID/CID/key.FMT      POST    comment_key
#api/item/IID/CID/key/KEY.FMT  DELETE  comment_key
#api/item/IID/CID/key/KEY.FMT  GET     comment_key
#api/item/IID/CID/key/KEY.FMT  PUT     comment_key
#api/item/IID/clone.FMT        GET     clone_list
#api/item/IID/clone.FMT        POST    clone
#api/item/IID/comment.FMT      GET     comment_list
#api/item/IID/comment.FMT      POST    comment
#api/item/IID/key.FMT          POST    item_key
#api/item/IID/key/KEY.FMT      DELETE  item_key
#api/item/IID/key/KEY.FMT      GET     item_key
#api/item/IID/key/KEY.FMT      PUT     item_key
#api/relation.FMT              GET     relation_list
#api/relation.FMT              POST    relation
#api/relation/RID.FMT          DELETE  relation
#api/relation/RID.FMT          GET     relation
#api/relation/RID/key.FMT      POST    relation_key
#api/relation/RID/key/KEY.FMT  DELETE  relation_key
#api/relation/RID/key/KEY.FMT  GET     relation_key
#api/relation/RID/key/KEY.FMT  PUT     relation_key
#api/tag.FMT                   GET     tag_list
#api/tag.FMT                   POST    tag
#api/tag/TID.FMT               DELETE  tag
#api/tag/TID.FMT               GET     tag
#api/tag/TID/key.FMT           POST    tag_key
#api/tag/TID/key/KEY.FMT       DELETE  tag_key
#api/tag/TID/key/KEY.FMT       GET     tag_key
#api/tag/TID/key/KEY.FMT       PUT     tag_key
#api/version.FMT               GET     version
#api/select/item.FMT             GET     x
#api/select/relation.FMT         GET     x
#api/select/tag.FMT              GET     x
#api/share/raw/RID/RVSN/IID.FMT  GET     x
#api/share/redirect/RID.FMT      GET     x
#api/share/redirect/RID/IID.FMT  GET     x
#api/share/url/RID.FMT           GET     x
#api/share/url/RID/IID.FMT       GET     x
#                               GET     x
#doc                            GET     doc
#doc/SUFFIX                     GET     doc
#get                            GET     get
#get                            POST    get
#pub                            GET     pub
#pub/SUFFIX                     GET     pub
#ui                             GET     x

ui/create-comment/IID.html      GET  create-comment
ui/create-item.html             GET  create-item
ui/create-relation.html         GET  create-relation
ui/create-tag.html              GET  create-tag
ui/delete-comment/IID/CID.html  GET  delete-comment
ui/delete-item/IID.html         GET  delete-item
ui/delete-relation/RID.html     GET  delete-relation
ui/delete-tag/TID.html          GET  delete-tag
ui/data/IID                     GET  data/IID
ui/list-comments/IID.html       GET  list-comments
ui/list-items.html              GET  list-items
ui/list-relations.html          GET  list-relations
ui/list-tags.html               GET  list-tags
ui/read-comment/IID/CID.html    GET  read-comment
ui/read-config.html             GET  read-config
ui/read-item/IID.html           GET  read-item
ui/read-relation/RID.html       GET  read-relation
ui/read-tag/TID.html            GET  read-tag
ui/update-comment/IID/CID.html  GET  update-comment
ui/update-config.html           GET  update-config
ui/update-item/IID.html         GET  update-item
ui/update-relation/RID.html     GET  update-relation
ui/update-tag/TID.html          GET  update-tag
ui/version.html                 GET  version.html