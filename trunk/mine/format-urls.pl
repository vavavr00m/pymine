#!/usr/bin/perl

%regexp_lookup = ( # $value text in <anglebrackets> must be same as lcase($key)
    'CID', '?P<cid>\d+',
    'FMT', '?P<fmt>(xml|json|py)',
    'IID', '?P<iid>\d+',
    'KEY', '?P<key>\w+',
    'RID', '?P<rid>\d+',
    'RVSN', '?P<rvsn>\d+',
    'SUFFIX', '?P<suffix>.+',
    'TID', '?P<tid>\d+',
    );

while (<DATA>) {
    if (/^\s*(\#.*)?$/o) {
        # skip comments and blank lines
        next;
    }

    ($class, $http_method, $url, $pymethod) = split;

    $output = \@{$text{'views'}{$class}};

    $pymethod =~ tr!-!_!;

    $callback = "$class.$pymethod";

    $pattern = $url;

    $pattern =~ s/([A-Z]+)/"(" . ($regexp_lookup{$1}||"&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& $1 &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&") . ")"/goe;

    @kwds = grep(/^[A-Z]+$/o, split(/\b/o, $url));

    @kwds = map { lc($_) } grep(!/^(FMT)$/o, @kwds);

    $aaa = join(", ", 'request', @kwds, '*args', '**kwargs');

    push(@{$output}, "## rest: $http_method $url\n");
    push(@{$output}, "## function: $pymethod\n");
    push(@{$output}, "## declared args: @kwds\n");
    push(@{$output}, "def $pymethod($aaa):\n");

    if ($class eq 'api') {
        push(@{$output}, "    raise Http404('method $pymethod for url $url is not yet implemented') # TO BE DONE\n");
        push(@{$output}, "    return { 'status': 'not yet implemented' }\n");
    }
    elsif ($class eq 'ui') {
        push(@{$output}, "    raise Http404('method $pymethod for url $url is not yet implemented') # TO BE DONE\n");
        push(@{$output}, "    return render_to_response('$suffix.html')\n");
    }

    push(@{$output}, "\n");

    push(@{$patterns{$pattern}}, "'$http_method': $callback");

    $class_of{$pattern} = $class;

}

##################################################################

$indent = "    ";

foreach $pattern (sort keys %patterns) {

    $class = $class_of{$pattern};

    $output = \@{$text{'urls'}{$class}};

    $foo = join(", ", @{$patterns{$pattern}});

    if ($class eq 'api') {
        $dispatch = "API_CALL";
    }
    else {
        $dispatch = "REST";
    }

    push(@{$output}, $indent, "(r'^$pattern\$', $dispatch,\n$indent {$foo}),\n");
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

# note: the /key/ thing is needed because of risk of /item/IID/KEY.FMT
# clashing with the /item/IID/comment.FMT namespace, and any other
# namespaces that may arise; and thus for orthogonality...

api   GET     /api/item/IID                    read-item-data

##################################################################

api   GET     /api/item.FMT                    read-item-list
api   POST    /api/item.FMT                    create-item
api   DELETE  /api/item/IID.FMT                delete-item
api   GET     /api/item/IID.FMT                read-item
api   POST    /api/item/IID.FMT                update-item
api   DELETE  /api/item/IID/key/KEY.FMT        delete-item-key
api   GET     /api/item/IID/key/KEY.FMT        get-item-key

##################################################################

api   GET     /api/relation.FMT                read-relation-list
api   POST    /api/relation.FMT                create-relation
api   DELETE  /api/relation/RID.FMT            delete-relation
api   GET     /api/relation/RID.FMT            read-relation
api   POST    /api/relation/RID.FMT            update-relation
api   DELETE  /api/relation/RID/key/KEY.FMT    delete-relation-key
api   GET     /api/relation/RID/key/KEY.FMT    get-relation-key

##################################################################

api   GET     /api/tag.FMT                     read-tag-list
api   POST    /api/tag.FMT                     create-tag
api   DELETE  /api/tag/TID.FMT                 delete-tag
api   GET     /api/tag/TID.FMT                 read-tag
api   POST    /api/tag/TID.FMT                 update-tag
api   DELETE  /api/tag/TID/key/KEY.FMT         delete-tag-key
api   GET     /api/tag/TID/key/KEY.FMT         get-tag-key

##################################################################

api   GET     /api/item/IID/comment.FMT        read-comment-list
api   POST    /api/item/IID/comment.FMT        create-comment
api   DELETE  /api/item/IID/CID.FMT            delete-comment
api   GET     /api/item/IID/CID.FMT            read-comment
api   POST    /api/item/IID/CID.FMT            update-comment
api   DELETE  /api/item/IID/CID/key/KEY.FMT    delete-comment-key
api   GET     /api/item/IID/CID/key/KEY.FMT    get-comment-key

##################################################################

api   GET     /api/item/IID/clone.FMT          read-clone-list
api   POST    /api/item/IID/clone.FMT          create-clone

##################################################################

api   GET     /api/registry.FMT                read-registry
api   POST    /api/registry.FMT                update-registry
api   DELETE  /api/registry/key/KEY.FMT        delete-registry-key
api   GET     /api/registry/key/KEY.FMT        get-registry-key

##################################################################

api   GET     /api/select/item.FMT             read-select-item
api   GET     /api/select/relation.FMT         read-select-relation
api   GET     /api/select/tag.FMT              read-select-tag

##################################################################

api   GET     /api/url/RID.FMT                 encode-minekey1
api   GET     /api/url/RID/IID.FMT             encode-minekey2
api   GET     /api/url/RID/RVSN/IID.FMT        encode-minekey3

##################################################################

api   GET     /api/version.FMT                 read-version

##################################################################

get   GET     /get/SUFFIX                      read-minekey
get   POST    /get/SUFFIX                      submit-minekey

##################################################################

mine  GET     /                                read-root-mine
mine  GET     /api                             read-root-api
mine  GET     /doc                             read-root-doc
mine  GET     /get                             read-root-get
mine  GET     /pub                             read-root-pub
mine  GET     /ui                              read-root-ui

##################################################################

ui    GET     /ui/create-comment/IID.html      create-comment
ui    GET     /ui/create-item.html             create-item
ui    GET     /ui/create-relation.html         create-relation
ui    GET     /ui/create-tag.html              create-tag
ui    GET     /ui/delete-comment/IID/CID.html  delete-comment
ui    GET     /ui/delete-item/IID.html         delete-item
ui    GET     /ui/delete-relation/RID.html     delete-relation
ui    GET     /ui/delete-tag/TID.html          delete-tag
ui    GET     /ui/list-comments/IID.html       list-comments
ui    GET     /ui/list-items.html              list-items
ui    GET     /ui/list-relations.html          list-relations
ui    GET     /ui/list-tags.html               list-tags
ui    GET     /ui/read-comment/IID/CID.html    read-comment
ui    GET     /ui/read-item/IID.html           read-item
ui    GET     /ui/read-registry.html           read-registry
ui    GET     /ui/read-relation/RID.html       read-relation
ui    GET     /ui/read-tag/TID.html            read-tag
ui    GET     /ui/update-comment/IID/CID.html  update-comment
ui    GET     /ui/update-item/IID.html         update-item
ui    GET     /ui/update-registry.html         update-registry
ui    GET     /ui/update-relation/RID.html     update-relation
ui    GET     /ui/update-tag/TID.html          update-tag
ui    GET     /ui/version.html                 version

##################################################################
