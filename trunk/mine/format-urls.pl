#!/usr/bin/perl

$indent = "    ";

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

    $template_prefix = $pymethod;

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

    push(@{$output}, "${indent}raise Http404('backend $pymethod for $http_method $url is not yet implemented') # TO BE DONE\n");

    if (($class eq 'api') and ($url ne '/api')) { # root
        push(@{$output}, "${indent}return { 'status': 'not yet implemented' }\n");
    }
    else {
        push(@{$output}, "${indent}return render_to_response('$template_prefix.html')\n");
    }

    push(@{$output}, "\n");

    push(@{$patterns{$pattern}}, "'$http_method': $callback");

    $class_of{$pattern} = $class;

}

##################################################################

foreach $pattern (sort {$b cmp $a} keys %patterns) {

    $class = $class_of{$pattern};

    $output = \@{$text{'urls'}{$class}};

    $foo = join(", ", @{$patterns{$pattern}});

    if (($class eq 'api') && ($pattern =~ /fmt/)) {
        $dispatch = "API_CALL";
    }
    else {
        $dispatch = "REST";
    }

    $pattern =~ s!^/(api|get|ui)!!o;
    $pattern =~ s!^/!!o;

    $dispatch = "REST" if ($pattern eq ''); # root

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

mine  GET     /                                read-mine-root
mine  GET     /doc                             read-doc-root
mine  GET     /pub                             read-pub-root

sys   GET     /export                          mine-export
sys   GET     /import                          mine-import
sys   GET     /cleanup                         mine-cleanup

##################################################################

api   GET     /api                             read-api-root
get   GET     /get                             read-get-root
ui    GET     /ui                              read-ui-root

##################################################################

api   GET     /api/item/IID                    read-item-data

##################################################################
api   GET     /api/item.FMT                    list-items
api   POST    /api/item.FMT                    create-item
api   DELETE  /api/item/IID.FMT                delete-item
api   GET     /api/item/IID.FMT                read-item
api   POST    /api/item/IID.FMT                update-item
api   DELETE  /api/item/IID/KEY.FMT            delete-item-key
api   GET     /api/item/IID/KEY.FMT            get-item-key

##################################################################

api   GET     /api/relation.FMT                list-relations
api   POST    /api/relation.FMT                create-relation
api   DELETE  /api/relation/RID.FMT            delete-relation
api   GET     /api/relation/RID.FMT            read-relation
api   POST    /api/relation/RID.FMT            update-relation
api   DELETE  /api/relation/RID/KEY.FMT        delete-relation-key
api   GET     /api/relation/RID/KEY.FMT        get-relation-key

##################################################################

api   GET     /api/tag.FMT                     list-tags
api   POST    /api/tag.FMT                     create-tag
api   DELETE  /api/tag/TID.FMT                 delete-tag
api   GET     /api/tag/TID.FMT                 read-tag
api   POST    /api/tag/TID.FMT                 update-tag
api   DELETE  /api/tag/TID/KEY.FMT             delete-tag-key
api   GET     /api/tag/TID/KEY.FMT             get-tag-key

##################################################################

api   GET     /api/comment/item/IID.FMT        list-comments
api   POST    /api/comment/item/IID.FMT        create-comment
api   DELETE  /api/comment/CID.FMT             delete-comment
api   GET     /api/comment/CID.FMT             read-comment
api   POST    /api/comment/CID.FMT             update-comment
api   DELETE  /api/comment/CID/KEY.FMT         delete-comment-key
api   GET     /api/comment/CID/KEY.FMT         get-comment-key

##################################################################

api   GET     /api/item/IID/clone.FMT          list-clones
api   POST    /api/item/IID/clone.FMT          create-clone

##################################################################

api   GET     /api/registry.FMT                read-registry
api   POST    /api/registry.FMT                update-registry
api   DELETE  /api/registry/KEY.FMT            delete-registry-key
api   GET     /api/registry/KEY.FMT            get-registry-key

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

get   GET     /get/KEY                         read-minekey
get   POST    /get/KEY                         submit-minekey

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
