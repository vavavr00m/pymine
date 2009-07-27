#!/usr/bin/perl

%lookup = (
    'CID', '\d+',
    'FMT', 'xml|json',
    'IID', '\d+',
    'RID', '\d+',
    'RVSN', '\d+',
    'SUFFIX', '.+',
    'TID', '\d+',
    );


while (<DATA>) {
    ($url, $method, @crap) = split;
    push(@{$foo{$url}}, $method);
}

END {
    foreach $url (sort keys %foo) {

	@bar = sort @{$foo{$url}};
	@bar = map { "'$_': None" } @bar;
	$baz = join(', ', @bar);
	$indent = "    ";

	1 while ($url =~ s/([A-Z]+)/"(".($lookup{$1} || "-----------------").")"/goe);

	print "$indent(r'^$url\$', views.rest, {$baz})\n";
    }
}

__END__;
/ GET 
/api/config.FMT POST 
/api/config.json GET 
/api/item.FMT GET 
/api/item.FMT POST 
/api/item/IID GET 
/api/item/IID PUT 
/api/item/IID.FMT DELETE 
/api/item/IID.FMT GET 
/api/item/IID/CID.FMT DELETE 
/api/item/IID/CID.FMT GET 
/api/item/IID/CID/key.FMT POST 
/api/item/IID/CID/key/KEY.FMT DELETE 
/api/item/IID/CID/key/KEY.FMT GET 
/api/item/IID/CID/key/KEY.FMT PUT 
/api/item/IID/clone.FMT GET 
/api/item/IID/clone.FMT POST 
/api/item/IID/comment.FMT GET 
/api/item/IID/comment.FMT POST 
/api/item/IID/key.FMT POST 
/api/item/IID/key/KEY.FMT DELETE 
/api/item/IID/key/KEY.FMT GET 
/api/item/IID/key/KEY.FMT PUT 
/api/relation.FMT GET 
/api/relation.FMT POST 
/api/relation/RID.FMT DELETE 
/api/relation/RID.FMT GET 
/api/relation/RID/key.FMT POST 
/api/relation/RID/key/KEY.FMT DELETE 
/api/relation/RID/key/KEY.FMT GET 
/api/relation/RID/key/KEY.FMT PUT 
/api/select/item.FMT GET 
/api/select/relation.FMT GET 
/api/select/tag.FMT GET 
/api/share/raw/RID/RVSN/IID.FMT GET 
/api/share/redirect/RID.FMT GET 
/api/share/redirect/RID/IID.FMT GET 
/api/share/url/RID.FMT GET 
/api/share/url/RID/IID.FMT GET 
/api/tag.FMT GET 
/api/tag.FMT POST 
/api/tag/TID.FMT DELETE 
/api/tag/TID.FMT GET 
/api/tag/TID/key.FMT POST 
/api/tag/TID/key/KEY.FMT DELETE 
/api/tag/TID/key/KEY.FMT GET 
/api/tag/TID/key/KEY.FMT PUT 
/api/version.FMT GET 
/doc GET 
/doc/SUFFIX GET 
/get GET 
/get POST 
/pub GET 
/pub/SUFFIX GET 
/ui GET 
/ui/SUFFIX GET 
/ui/bulk-tags.html POST
/ui/clone-item/IID.html DUMMY
/ui/create-item.html GET 
/ui/create-item.html POST
/ui/create-relation.html DUMMY
/ui/create-relation.html POST
/ui/create-tag.html DUMMY
/ui/create-tag.html POST
/ui/delete-item/IID.html DUMMY
/ui/delete-relation/RID.html GET 
/ui/delete-tag/TID.html GET 
/ui/get-item/IID.html GET 
/ui/get-relation/RID.html GET 
/ui/get-tag/TID.html GET 
/ui/list-clones/IID.html GET 
/ui/list-items.html GET 
/ui/list-relations.html GET 
/ui/list-tags.html GET 
/ui/select/item.html GET 
/ui/select/relation.html GET 
/ui/select/tag.html GET 
/ui/share/raw/RID/RVSN/IID GET 
/ui/share/redirect/RID GET 
/ui/share/redirect/RID/IID GET 
/ui/share/url/RID.html GET 
/ui/share/url/RID/IID.html GET 
/ui/show-config.html GET 
/ui/update-config.html GET 
/ui/update-data/IID.html GET 
/ui/update-item/IID.html GET 
/ui/update-item/IID.html POST
/ui/update-relation/RID.html DUMMY
/ui/update-relation/RID.html POST
/ui/update-tag/TID.html DUMMY
/ui/update-tag/TID.html POST
/ui/version.html GET
