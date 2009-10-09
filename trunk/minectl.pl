#!/usr/bin/perl

##
## Copyright 2008-09 Adriana Lukas & Alec Muffett
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

# declarations
our $MINE_HTTP_FULLPATH = "http://127.0.0.1:9862";
my ($d, $j, $a);

# use imported values
$root = $MINE_HTTP_FULLPATH;

#------------------------------------------------------------------

# load the MIME lookup library
sub mime_type {
    my $filesuffix = shift;
    $filesuffix =~ s!^.*\.!!o; # greedy match to destroy as much as possible
    $filesuffix =~ tr/A-Z/a-z/; # force lowercase

    # start by fast-tracking certain extensions
    # approximate order of likliehood
    return "text/html" if ($filesuffix eq 'html');
    return "image/jpeg" if ($filesuffix eq 'jpg');
    return "image/png" if ($filesuffix eq 'png');
    return "text/css" if ($filesuffix eq 'css');
    return "text/plain" if ($filesuffix eq 'txt');
    return "image/gif" if ($filesuffix eq 'gif');
    return "image/jpeg" if ($filesuffix eq 'jpeg');
    return "text/html" if ($filesuffix eq 'htm');

    # insert a mime.types lookup here
    my $mimefile = "static/mime.types";

    open(MIME, $mimefile) || die "open: $mimefile: $!\n";
    while (<MIME>) {
        next if m!^\s*(\#.*)?$!o;
        my ($type, @suffixes) = split;
        foreach my $suffix (@suffixes) {
            if ($suffix eq $filesuffix) {
                return $type;
            }
        }
    }
    close(MIME);

    # fall through
    return "application/octet-stream";
}

#------------------------------------------------------------------

##################################################################

# basic argument parsing

my %FLAGDESC = (
    e => '# print error-page upon HTTP error (side effect: sets exit status to 0)',
    h => '# help mode; use also "help" command',
    x => '# XML output, if possible',
    r => '# RAW output, if possible',
    q => '# do NOT quit upon curl returning an error code',
    u => '[username:password] # authentication',
    v => '# verbose; -vv, -vvv = more verbose',
    );

my %FLAG;

while ($ARGV[0] =~ m!^-(\w+)!o) {
    my $switches = $1;

    foreach my $switch (split(//o, $switches)) {
	if ($switch eq 'v') {
	    $FLAG{'verbose'}++;
	}
	elsif ($switch eq 'x') {
	    $FLAG{'xml'} = 1;
	}
	elsif ($switch eq 'h') {
	    $FLAG{'help'} = 1;
	}
	elsif ($switch eq 'r') {
	    $FLAG{'raw'} = 1;
	}
	elsif ($switch eq 'q') {
	    $FLAG{'dontquit'} = 1;
	}
	elsif ($switch eq 'e') {
	    $FLAG{'curlerrs'} = 1;
	}
	elsif ($switch eq 'u') {
	    shift(@ARGV); # dump the -u
	    $FLAG{'userpass'} = $ARGV[0];
	}
	else {
	    die "$0: unknown option $switch (fatal)\n";
	}
    }

    shift;
}


if ($FLAG{'verbose'} >= 3) {
    push(@curlopts, '--verbose'); # make curl act verbosely
}

# default make curl die silently / set errno upon failure
unless ($FLAG{'curlerrs'}) {
    push(@curlopts, '--fail');	
}

if ($FLAG{'userpass'}) {
    # curl user and pw for authentication
    push(@curlopts, '--user', $FLAG{'userpass'});
    push(@curlopts, '--basic');
}

# verbal way to request help

if ($ARGV[0] eq 'help') {
    $FLAG{'help'} = 1;
    shift;
}

##################################################################

my $usercmd = shift;
my @cmdlist = ();
my $we_did_something = 0;

##################################################################

if ($FLAG{'help'}) {
    if (!defined($usercmd)) {
	$FLAG{'help'} = 0;	# no pattern, drop thru to std message
    }
    else {
	print "help: all commands matching /$usercmd/\n";
    }
}

while (<DATA>) {
    next if (/^\s*(\#.*)?$/o);  # skip comment lines and blanks
    s/\#.*$//go;                # strip comments
    s/\s+/ /go;                 # strip multi-whitespace
    s/\s$//o;;                  # strip trailing whitespace

    # split on spaces
    my ($cmd, $call_how, $method, $api, $doc) = split(" ", $_, 5);

    # for use in the help string, below; self-documenting code my arse
    push(@cmdlist, "\t$cmd $doc\n");

    # help kludge
    if ($FLAG{'help'}) {
	print "\t$cmd $doc\n" if ("$cmd $doc" =~ m!$usercmd!i);
	$we_did_something = 1;
	next;
    }

    # if this is not it, then skip to next
    next unless ($usercmd eq $cmd);

    # remember we tried to do something
    $we_did_something = 1;

    # PASSARGS: apply all foo=bar keys to single API call

    if ($call_how eq 'PASSARGS') {
	&Mine($method, $api, @ARGV);
    }

    # ITERARGS: apply each foo=bar key to individual API calls

    elsif ($call_how eq 'ITERARGS') {
	foreach $arg (@ARGV) {
	    &Mine($method, $api, $arg);
	}
    }

    # SUB1PASS: strip the first arg and interpolate into API URL; pass
    # all subsequent foo=bar keys to it ; THIS IS PRIBABLY SAFEST CASE
    # FOR SINGLE-ARGUMENT COMMANDLINES.

    elsif ($call_how eq 'SUB1PASS') {
	my $arg = shift;
	$api =~ s!\b([RITCV]ID|KEY)\b!$arg!g;
	&Mine($method, $api, @ARGV);
    }

    # SUB1ITER: strip the first arg and interpolate into API URL;
    # apply each subsequent foo=bar key to it individually

    elsif ($call_how eq 'SUB1ITER') {
	my $id = shift;
	$api =~ s![RITCV]ID!$id!g;
	foreach my $arg (@ARGV) {
	    &Mine($method, $api, $arg);
	}
    }

    # SUBEVERY: strip each arg and interpolate it into an API URL, and
    # call that without keys

    elsif ($call_how eq 'SUBEVERY') {
	foreach $arg (@ARGV) {
	    my $api2 = $api;
	    $api2 =~ s![RITCV]ID!$arg!g;
	    &Mine($method, $api2);
	}
    }

    # SUB1EVERY: strip the first arg and interpolate into API URL;
    # strip each remaining arg and interpolate it into the API URL,
    # and call that without keys

    elsif ($call_how eq 'SUB1EVERY') {
	my $id = shift;
	$api =~ s![RITCV]ID!$id!g;
	foreach $arg (@ARGV) {
	    my $api2 = $api;
	    $api2 =~ s!KEY!$arg!g;
	    &Mine($method, $api2);
	}
    }

    # SUB2PASS: strip the first two args (1=ID 2=KEY) and interpolate
    # into API URL; pass all subsequent foo=bar keys to it

    elsif ($call_how eq 'SUB2PASS') {
	my $arg = shift;
	my $id = shift;
	$api =~ s!\b([RITCV]ID)\b!$arg!g;
	$api =~ s!\b(KEY)\b!$id!g;
	&Mine($method, $api, @ARGV);
    }

    # FRELATION: magic special case for adding relations

    elsif ($call_how eq 'FRELATION') {

	my $relationname = shift(@ARGV);
	my $relationversion = shift(@ARGV);
	my $relationdescription = shift(@ARGV);

	&Mine($method,
	      $api,
	      "relationName=$relationname",
	      "relationVersion=$relationversion",
	      "relationDescription=$relationdescription",
	      "relationInterests=@ARGV",
	    );
    }

    # FUPLOAD: magic special case for uploading files

    elsif ($call_how eq 'FUPLOAD') {
	my $tags = undef;
	my $status = undef;

	while ($ARGV[0] =~ /^-/o) {
	    if ($ARGV[0] eq '-t') {
		shift(@ARGV);	      # dump -t
		$tags = shift(@ARGV); # stash and dump the arg
	    }
	    elsif ($ARGV[0] eq '-s') {
		shift(@ARGV);		# dump -s
		$status = shift(@ARGV); # stash and dump the arg
		unless ($status =~ /^(public|shared|private)$/o) {
		    die "$0: upload: bad status $status (fatal)\n";
		}
	    }
	    else {
		die "$0: upload: unknown argument $ARGV[0] (fatal)\n";
	    }
	}

	foreach my $filename (@ARGV) {
	    my $filetype = &mime_type($filename);
	    $itemname = $filename;
	    $itemname =~ s!^.*/!!o;
	    my @cmdargs = (
		"itemData=\@$filename",
		"itemName=$itemname",
		"itemType=$filetype",
		"itemDescription=auto-uploaded from $filename"
		);

	    if (defined($status)) {
		push(@cmdargs, "itemStatus=$status");
	    }
	    else {
		push(@cmdargs, "itemStatus=public");
	    }

	    if (defined($tags)) {
		push(@cmdargs, "itemTags=$tags");
	    }

	    &Mine($method, $api, @cmdargs);
	}
    }

    # FTAGS: magic special case for creating tags

    elsif ($call_how eq 'FTAGS') {

	foreach my $foo (@ARGV) {
	    my ($tagname, $tagparents) = split(m!:!o, $foo);
	    my (@tagimplies) = split(m!,!o, $tagparents);
	    my @tagargs = ();

	    push(@tagargs, "tagName=$tagname");
	    push(@tagargs, "tagImplies=@tagimplies") if ($#tagimplies >= 0);
	    &Mine($method, $api, @tagargs);
	}
    }

    # MIMETYPE: useful kludge

    elsif ($call_how eq 'MIMETYPE') {

	foreach my $filename (@ARGV) {
	    my $filetype = &mime_type($filename);
	    print "$filetype\n";
	}
    }

    # THIS CAN'T HAPPEN

    else {
	die "LOL WHUT? (fatal)\n";
    }
}

##################################################################

# did the user goof?

unless ($we_did_something) {

    warn "usage:\t$0 [options] command [cmdoptions] [args ... ]\n";
    warn "options:\n";
    foreach my $f (sort keys %FLAGDESC) {
	warn "\t-$f $FLAGDESC{$f}\n";
    }
    warn "commands:\n";
    warn "\thelp [keyword]\n";
    warn join ('',  sort @cmdlist);
    exit 1;
}

##################################################################

# done
exit 0;

##################################################################
##################################################################
##################################################################

# that which calls curl
sub Mine {
    my ($method, $api, @args) = @_;
    my $query;
    my @curlargs;

    if ($method eq 'create') {
	push(@curlopts, '-X', "POST");
	$query = "";
    }
    elsif ($method eq 'read') {
	push(@curlopts, '-X', "GET");
	$query = "";
    }
    elsif ($method eq 'update') {
	push(@curlopts, '-X', "PUT");
	$query = "";
    }
    elsif ($method eq 'delete') {
	push(@curlopts, '-X', "DELETE");
	$query = "";
    }
    else {
	die "$0: unrecognised method $method (fatal)\n";
    }

    foreach $arg (@args) {
	push(@curlargs, '-F', $arg);
    }

    if ($FLAG{'xml'}) {
	# only swap to .xml if was .json beforehand
	unless ($api =~ s!\.json$!.xml!o) {
	    die "$0: API $api cannot be coersced to XML format output (fatal)\n";
	}
    }

    if ($FLAG{'raw'}) {
	# only swap to .raw if was .json beforehand
	unless ($api =~ s!\.json$!.raw!o) {
	    die "$0: API $api cannot be coersced to RAW format output (fatal)\n";
	}
    }

    @cmd = ("curl", @curlopts, "$root$api$query", @curlargs);

    warn "+ exec: @cmd\n" if ($FLAG{'verbose'} >= 1);

    my $retval = system(@cmd);
    my $retval2 = $retval >> 8;

    unless ($FLAG{'dontquit'}) {
	die "$0: curl returned exit status $retval2 (fatal)\n" if ($retval);
    }

    warn "+ curl returned exit status $retval2 (info)\n" if ($FLAG{'verbose'} >= 2);
}

##################################################################
##################################################################
##################################################################
__END__;

# useful hacks
mime-type MIMETYPE - - filename.ext ...

# accelerated upload
upload FUPLOAD create /api/item.json [-t "tag ..."] [-s status] item.jpg item.pdf ...

# accelerated tagging
new-tags FTAGS create /api/tag.json tag1 tag2 tag3:implies1 tag4:implies1,implies2[,more...] ...

# accelerated relation
new-relation FRELATION create /api/relation.json name vers desc tag ...

###
# raw API calls
###

# calling the feed and item retreival
get SUB1PASS read /get/KEY minekey

# the version command, effectively a no-op / test routine
version PASSARGS read /api/version.json

# all instances of update-foo (except update-data) were more formally
# "create-foo-key" method calls; this is because there is no API
# interface to support modifying a Thing (Relation / Item / Tag /
# Comment / Config) by means of replacing one binary blob with
# another; thus the more refined create-foo-key routines were
# hijacked to achieve the intended aim of update-foo...

get-comment SUB1PASS read /api/comment/CID.json 42
delete-comment SUBEVERY delete /api/comment/CID.json 42 27 23 ...
update-comment SUB1PASS create /api/comment/CID.json 42 commentKey=value ...
get-comment-key SUB1EVERY read /api/comment/CID/KEY.json 42 commentKey
delete-comment-key SUB1EVERY delete /api/comment/CID/KEY.json 42 commentKey ...
list-comments SUBEVERY read /api/comment/item/IID.json
create-comment SUB1PASS create /api/comment/item/IID.json commentKey=value ...


list-registry PASSARGS read /api/registry.json
get-registry-key SUB1PASS read /api/registry/IID.json key
update-registry-key SUB1PASS create /api/registry/IID.json key=value
delete-registry-key SUB1EVERY delete /api/registry/IID.json

get-config PASSARGS read /api/config.json
update-config PASSARGS create /api/config.json key=value ...

list-items PASSARGS read /api/item.json
create-item PASSARGS create /api/item.json itemData=@filename.txt itemKey=value ...
get-data SUB1PASS read /api/item/IID 42
get-item SUB1PASS read /api/item/IID.json 42
delete-item SUBEVERY delete /api/item/IID.json 42 17 23 ...
update-item SUB1PASS create /api/item/IID.json 42 itemKey=value ...
get-item-key SUB1EVERY read /api/item/IID/KEY.json 42 itemKey
delete-item-key SUB1EVERY delete /api/item/IID/KEY.json 42 itemKey ...

clone-item SUB1PASS create /api/item/IID/clone.json 42
list-clones SUB1PASS read /api/item/IID/clone.json 42

list-relations PASSARGS read /api/relation.json
create-relation PASSARGS create /api/relation.json relationKey=value ...
get-relation SUB1PASS read /api/relation/RID.json 42
delete-relation SUBEVERY delete /api/relation/RID.json 42 17 23 ...
update-relation SUB1PASS create /api/relation/RID.json 42 relationKey=value ...
get-relation-key SUB1EVERY read /api/relation/RID/KEY.json 42 relationKey
delete-relation-key SUB1EVERY delete /api/relation/RID/KEY.json 42 relationKey ...

list-tags PASSARGS read /api/tag.json
create-tag PASSARGS create /api/tag.json tagKey=value ...
get-tag SUB1PASS read /api/tag/TID.json 42
delete-tag SUBEVERY delete /api/tag/TID.json 42 17 23 ...
update-tag SUB1PASS create /api/tag/TID.json 42 tagKey=value ...
get-tag-key SUB1EVERY read /api/tag/TID/KEY.json 42 tagKey
delete-tag-key SUB1EVERY delete /api/tag/TID/KEY.json 42 tagKey ...

list-vurls PASSARGS read /api/vurl.json
create-vurl PASSARGS create /api/vurl.json vurlKey=value ...
get-vurl SUB1PASS read /api/vurl/VID.json 42
delete-vurl SUBEVERY delete /api/vurl/VID.json 42 17 23 ...
update-vurl SUB1PASS create /api/vurl/VID.json 42 vurlKey=value ...
get-vurl-key SUB1EVERY read /api/vurl/VID/KEY.json 42 vurlKey
delete-vurl-key SUB1EVERY delete /api/vurl/VID/KEY.json 42 vurlKey ...
