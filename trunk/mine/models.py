#!/usr/bin/python
##
## Copyright 2009 Adriana Lukas & Alec Muffett
##
## Licensed under the Apache License, Version 2.0 (the "License"); you
## may not use this file except in compliance with the License. You
## may obtain a copy of the License at
##
## http://www.apache.org/licenses/LICENSE-2.0
##
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
## implied. See the License for the specific language governing
## permissions and limitations under the License.
##

import itertools

from django.db import models, transaction
from django.core.files.storage import FileSystemStorage
from django.conf import settings

# The transcoder methods below provide a lot of the security for
# pymine, and govern the movement of data between three 'spaces" of
# data representation; these are:

# r-space - request space, where data are held in a HttpRequest
# s-space - structure space, where data are held in a dict
# m-space - model space, where data are fields in model instances

# The reason for keeping two spaces is partly philosophic - that there
# should be a clearly defined breakpoint between the two worlds, and
# this is it; if we just serialized models and slung them back and
# forth, the mine would be wedded to Django evermore, which is not a
# good thing. 

# Further: certain s-space attributes (eg: 'relationInterests') map to
# more than one m-space attributes, so these functions provide parsing
# as well as translation.

# r-space and s-space share exactly the same naming conventions, ie:
# they use camelCase keys such as "relationName" and "tagDescription"
# and "itemId" to label data; the only meaningful difference is that
# in r-space all data are held in HttpRequest objects as strings; when
# pulled into s-space Python dictionaries, any data which are integers
# (eg: itemId) are converted to Python integers.

# For obvious reasons it's never necessary to go from s-space to
# r-space; instead data only ever comes *out* of HttpRequests and
# *into* structures, hence there are only r2s_foo methods, and indeed
# only two of those: r2s_str and r2s_int:

def r2s_str(r, rname, s):
    """get rname from HttpRequest r's r.REQUEST and populate structure s with it"""
    if rname in r.REQUEST: 
        s[rname] = r.REQUEST[rname]

def r2s_int(r, rname, s):
    """get rname from HttpRequest r's r.REQUEST and populate structure s with it after converting to int"""
    if rname in r.REQUEST: 
        s[rname] = int(r.REQUEST[rname])

# Transfers between s-space (dictionary entries such as s['itemId'])
# and m-space (m.id, where 'm' is a instance of the Item model and
# 'id' is the Item table primary key) are bidirectional; because
# m-space and s-space both frequently use strings and python integers,
# and since s-space uses Python ints, many transfers can be handled
# with simple blind copies using introspection to access the model
# instance.

# Note: as a general rule m2s routines should not copy-out a None
# item, blank or null reference; however s2m routines *may* want to
# copy-in 'None' for purposes of erasure.  All copy routines should
# check the validity of their source/destination attributes.

# XXX: TBD: COPYING NONE FOR S2M THROUGHOUT

def m2s_copy(m, mattr, s, sattr):
    """Copy mattr from m to sattr in s"""
    x = getattr(m, mattr)
    s[sattr] = x

def s2m_copy(s, sattr, m, mattr):
    """Copy sattr from s to mattr in m"""
    if sattr in s:
        setattr(m, mattr, s[sattr])

# Because a lot of our code is table-driven, it helps to have a couple
# of dummy routines as filler where beneficial:

def m2s_dummy(m, mattr, s, sattr):
    """Barfing Placeholder"""
    raise Exception, 'something invoked m2s_dummy'

def s2m_dummy(s, sattr, m, mattr):
    """Barfing Placeholder"""
    raise Exception, 'something invoked s2m_dummy'

# One of the more complex translations between spaces are DateTime
# objects; in m-space we use whatever Django mandates, and in s-space
# we use a string representation of the time/date in ISO format, which
# is very close to what ATOM specifies - which in turn is probably
# what we will standardise on eventually

def m2s_date(m, mattr, s, sattr):
    """Copy a DateTime from m to a isoformat string in s"""
    x = getattr(m, mattr)
    if x: 
        s[sattr] = x.isoformat()

def s2m_date(s, sattr, m, mattr):
    if sattr in s: 
        raise Exception, "not yet integrated the Date parser"

# Specialist Type Conversion - Note: Where we are writing custom
# converters we don't generally bother to use introspection because we
# know the names of the model fields.

# The 'Comment' model has an 'item' field that is a ForeignKey
# representing the item-being-commented-upon; in s-space this is
# represented as the itemId being commented upon, an int.

def m2s_commentitem(m, mattr, s, sattr):
    if mattr != 'item' or sattr != 'commentItem': 
        raise Exception, "m2s_commentitem is confused"
    x = m.item
    if x: 
        s[sattr] = x.id

def s2m_commentitem(s, sattr, m, mattr):
    if mattr != 'item' or sattr != 'commentItem': 
        raise Exception, "s2m_commentitem is confused"
    if sattr in s: 
        m.item = Item.get(id=s[sattr]) # ITEM LOOKUP

# The 'Comment' model also has a 'relation' field that is a ForeignKey
# representing the relation-submitting-the-comment; in s-space this is
# represented as the relationName, a string

def m2s_commentrelation(m, mattr, s, sattr):
    if mattr != 'relation' or sattr != 'commentRelation': 
        raise Exception, "m2s_commentrelation is confused"
    x = m.relation
    if x: 
        s[sattr] = x.name

def s2m_commentrelation(s, sattr, m, mattr):
    if mattr != 'relation' or sattr != 'commentRelation': 
        raise Exception, "s2m_commentrelation is confused"
    if sattr in s: 
        m.relation = Relation.get(name=s[sattr]) # RELATION LOOKUP

# The 'Tag' model contains a ManyToMany field which cites the
# implications / multiple parents that any given Tag can have; in
# s-space this is represented as a space-separated string which
# contatenates tagNames.  Loops are possible, but benign.

def m2s_tagimplies(m, mattr, s, sattr):
    if mattr != 'implies' or sattr != 'tagImplies': 
        raise Exception, "m2s_tagimplies is confused"
    x = ' '.join([ x.name for x in m.implies.all() ])
    if x: 
        s[sattr] = x

def s2m_tagimplies(s, sattr, m, mattr):
    if mattr != 'implies' or sattr != 'tagImplies': 
        raise Exception, "s2m_tagimplies is confused"
    if sattr in s:
	for x in s[sattr].split():
            m.implies.add(Tag.objects.get(name=x))

# VirtualURL models contain very basic tagging for reference puproses;
# the model field is 'tags' and is a space-separated string which
# contatenates tagNames.

def m2s_vurltags(m, mattr, s, sattr):
    if mattr != 'tags' or sattr != 'vurlTags': 
        raise Exception, "m2s_vurltags is confused"
    x = ' '.join([ x.name for x in m.tags.all() ])
    if x: s[sattr] = x

def s2m_vurltags(s, sattr, m, mattr):
    if mattr != 'tags' or sattr != 'vurlTags': 
        raise Exception, "s2m_vurltags is confused"
    if sattr in s:
	for x in s[sattr].split(): m.implies.add(Tag.objects.get(name=x))

# itemStatus is a multi-choice field; the s-space representation of
# itemStatus ('public', 'shared', 'private') must be mapped back and
# forth to the single characters which are held in item.status

def m2s_itemstatus(m, mattr, s, sattr):
    if mattr != 'status' or sattr != 'itemStatus': 
        raise Exception, "s2m_itemtags is confused"
    s[sattr] = m.get_status_display()

def s2m_itemstatus(s, sattr, m, mattr):
    if mattr != 'status' or sattr != 'itemStatus': 
        raise Exception, "m2s_itemtags is confused"
    x = s[sattr]
    if x in status_lookup:
	setattr(m, mattr, status_lookup[x])
    else:
	raise Exception, "s2m_itemstatus cannot remap status: " + x

# itemTags is a complex tagging string: in s-space it is a
# space-separated string like "wine beer for:alice not:bob" where
# 'alice' and 'bob' are relationNames and 'wine' and 'beer' are
# tagNames; that data is parsed out and split into *three* separate
# m-space fields: m.tags, m.item_for_relations, m.item_not_relations -
# which are all ManyToMany fields.

def m2s_itemtags(m, mattr, s, sattr):
    if mattr != 'tags' or sattr != 'itemTags': 
        raise Exception, "m2s_itemtags is confused"

    # i like this bit of code
    x = " ".join(x for x in itertools.chain([ i.name for i in m.tags.all() ],
					    [ "for:%s" % i.name for i in m.item_for_relations.all() ],
					    [ "not:%s" % i.name for i in m.item_not_relations.all() ]))
    if x: 
        s[sattr] = x

def s2m_itemtags(s, sattr, m, mattr):
    if mattr != 'tags' or sattr != 'itemTags': 
        raise Exception, "s2m_itemtags is confused"
    if sattr in s:
	for x in s[sattr].split():
	    if x.startswith('for:'): m.item_for_relations.add(Tag.objects.get(name=x[4:]))
	    elif x.startswith('not:'): m.item_not_relations.add(Tag.objects.get(name=x[4:]))
	    else: m.tags.add(Tag.objects.get(name=x))


# relationInterests is another complex string: in s-space it is a
# space-separated string like "wine require:australia exclude:merlot"
# - the goal of which I hope is fairly clear, that a relation will
# take anything implicitly or explicitly tagged 'wine' but requires
# the 'australia' tag to be also present, rejecting anything that also
# includes the 'merlot' tag; in m-space this also breaks out into
# three fields: m.tags, m.tags_required, m.tags_excluded

def m2s_relationinterests(m, mattr, s, sattr):
    if mattr != 'interests' or sattr != 'relationInterests': 
        raise Exception, "m2s_relationinterests is confused"

    x = " ".join(x for x in itertools.chain([ i.name for i in m.tags.all() ],
					    [ "require:%s" % i.name for i in m.tags_required.all() ],
					    [ "exclude:%s" % i.name for i in m.tags_excluded.all() ]))
    if x: s[sattr] = x

def s2m_relationinterests(s, sattr, m, mattr):
    if mattr != 'interests' or sattr != 'relationInterests': 
        raise Exception, "s2m_relationinterests is confused"
    if sattr in s:
	for x in s[sattr].split():
	    if x.startswith('require:'): m.tags_required.add(Tag.objects.get(name=x[8:]))
	    elif x.startswith('exclude:'): m.tags_excluded.add(Tag.objects.get(name=x[8:]))
	    elif x.startswith('except:'): m.tags_excluded.add(Tag.objects.get(name=x[7:])) # common typo
	    else: m.tags.add(Tag.objects.get(name=x))

##################################################################

class Thing():
    key_prefix = None

    key_conversion = (
	( 'commentBody', 'body', False, r2s_str, s2m_copy, m2s_copy, ),
	( 'commentCreated', 'created', False, r2s_str, s2m_date, m2s_date, ),
	( 'commentId', 'id', False, r2s_int, s2m_copy, m2s_copy, ),
	( 'commentItem', 'item', True, r2s_int, s2m_commentitem, m2s_commentitem, ),
	( 'commentLastModified', 'last_modified', False, r2s_str, s2m_date, m2s_date, ),
	( 'commentLikes', 'likes', False, r2s_str, s2m_copy, m2s_copy, ),
	( 'commentRelation', 'relation', True, r2s_str, s2m_commentrelation, m2s_commentrelation, ),
	( 'commentTitle', 'title', False, r2s_str, s2m_copy, m2s_copy, ),
	( 'itemCreated', 'created', False, r2s_str, s2m_date, m2s_date, ),
	( 'itemData', 'data', True, None, s2m_dummy, None, ),
	( 'itemDescription', 'description', False, r2s_str, s2m_copy, m2s_copy, ),
	( 'itemHideAfter', 'hide_after', False, r2s_str, s2m_date, m2s_date, ),
	( 'itemHideBefore', 'hide_before', False, r2s_str, s2m_date, m2s_date, ),
	( 'itemId', 'id', False, r2s_int, s2m_copy, m2s_copy, ),
	( 'itemLastModified', 'last_modified', False, r2s_str, s2m_date, m2s_date, ),
	( 'itemName', 'name', False, r2s_str, s2m_copy, m2s_copy, ),
	( 'itemStatus', 'status', False, r2s_str, s2m_itemstatus, m2s_itemstatus, ),
	( 'itemTags', 'tags', True, r2s_str, s2m_itemtags, m2s_itemtags, ),
	( 'itemType', 'content_type', False, r2s_str, s2m_copy, m2s_copy, ),
	( 'relationCallbackURL', 'url_callback', False, r2s_str, s2m_copy, m2s_copy, ),
	( 'relationCreated', 'created', False, r2s_str, s2m_date, m2s_date, ),
	( 'relationDescription', 'description', False, r2s_str, s2m_copy, m2s_copy, ),
	( 'relationEmailAddress', 'email_address', False, r2s_str, s2m_copy, m2s_copy, ),
	( 'relationEmbargoAfter', 'embargo_after', False, r2s_str, s2m_date, m2s_date, ),
	( 'relationEmbargoBefore', 'embargo_before', False, r2s_str, s2m_date, m2s_date, ),
	( 'relationHomepageURL', 'url_homepage', False, r2s_str, s2m_copy, m2s_copy, ),
	( 'relationId', 'id', False, r2s_int, s2m_copy, m2s_copy, ),
	( 'relationImageURL', 'url_image', False, r2s_str, s2m_copy, m2s_copy, ),
	( 'relationInterests', 'interests', True, r2s_str, s2m_relationinterests, m2s_relationinterests, ),
	( 'relationLastModified', 'last_modified', False, r2s_str, s2m_date, m2s_date, ),
	( 'relationName', 'name', False, r2s_str, s2m_copy, m2s_copy, ),
	( 'relationNetworkPattern', 'network_pattern', False, r2s_str, s2m_copy, m2s_copy, ),
	( 'relationVersion', 'version', False, r2s_str, s2m_copy, m2s_copy, ),
	( 'tagCreated', 'created', False, r2s_str, s2m_date, m2s_date, ),
	( 'tagDescription', 'description', False, r2s_str, s2m_copy, m2s_copy, ),
	( 'tagId', 'id', False, r2s_int, s2m_copy, m2s_copy, ),
	( 'tagImplies', 'implies', True, r2s_str, s2m_tagimplies, m2s_tagimplies, ),
	( 'tagLastModified', 'last_modified', False, r2s_str, s2m_date, m2s_date, ),
	( 'tagName', 'name', False, r2s_str, s2m_copy, m2s_copy, ),
	( 'vurlCreated', 'created', False, r2s_str, s2m_date, m2s_date, ),
	( 'vurlId', 'id', False, r2s_int, s2m_copy, m2s_copy, ),
	( 'vurlLastModified', 'last_modified', False, r2s_str, s2m_date, m2s_date, ),
	( 'vurlLink', 'link', False, r2s_str, s2m_copy, m2s_copy, ),
	( 'vurlName', 'name', False, r2s_str, s2m_copy, m2s_copy, ),
	( 'vurlTags', 'tags', True, r2s_str, s2m_vurltags, m2s_vurltags, ),
	)

    def __unicode__(self):
	return self.name

    def to_structure(self):
	return model_to_structure(self.key_prefix, self)

    def get_structure_key(self, key):
	# check validity of key
	# lookup equivalent model field
	# retreive equivalent model field
	# convert to s-form and return
	pass

    def set_structure_key(self, key, value):
	# check validity of key
	# convert value to m-form
	# lookup equivalent model field
	# store m-form in model field
	# return original value
	pass

    def new_from_request(self, request):
	pass

    def update_from_request(self, request):
	pass

    def clone_from_request(self, request):
	pass

##################################################################

class Tag(models.Model, Thing):

    """This is the modelspace representation of the Tag object"""

    key_prefix = "tag"

    name = models.SlugField(max_length=settings.MINE_STRINGSIZE, unique=True)
    description = models.TextField(null=True, blank=True)
    implies = models.ManyToManyField('self', symmetrical=False, related_name='x_implies', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
	ordering = ['name']

##################################################################

class Relation(models.Model, Thing):

    """This is the modelspace representation of the Relation object"""

    key_prefix = "relation"

    name = models.SlugField(max_length=settings.MINE_STRINGSIZE, unique=True)
    description = models.TextField(null=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name='relations_with_tag', null=True, blank=True)
    tags_required = models.ManyToManyField(Tag, related_name='relations_requiring', null=True, blank=True)
    tags_excluded = models.ManyToManyField(Tag, related_name='relations_excluding', null=True, blank=True)
    version = models.PositiveIntegerField(default=1)
    embargo_after = models.DateTimeField(null=True, blank=True)
    embargo_before = models.DateTimeField(null=True, blank=True)
    network_pattern = models.CharField(max_length=settings.MINE_STRINGSIZE, blank=True)
    email_address = models.EmailField(max_length=settings.MINE_STRINGSIZE, blank=True)
    url_callback = models.URLField(max_length=settings.MINE_STRINGSIZE, blank=True)
    url_homepage = models.URLField(max_length=settings.MINE_STRINGSIZE, blank=True)
    url_image = models.URLField(max_length=settings.MINE_STRINGSIZE, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
	ordering = ['name']

##################################################################

class Item(models.Model, Thing):

    """This is the modelspace representation of the Item object"""

    key_prefix = "item"

    ITEM_FSS = FileSystemStorage(location=settings.MINE_DBDIR_FILES)

    ITEM_STATUSES=(
	( 'X', 'private' ),
	( 'S', 'shared' ),
	( 'P', 'public' ),
	#( 'A', 'authreqd' ),
	)

    for short, long in ITEM_STATUSES:
       status_lookup[long] = short

    name = models.CharField(max_length=settings.MINE_STRINGSIZE)
    description = models.TextField(null=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name='items_tagged', null=True, blank=True)
    item_for_relations = models.ManyToManyField(Relation, related_name='items_explicitly_for', null=True, blank=True)
    item_not_relations = models.ManyToManyField(Relation, related_name='items_explicitly_not', null=True, blank=True)
    status = models.CharField(max_length=1, choices=ITEM_STATUSES)
    content_type = models.CharField(max_length=settings.MINE_STRINGSIZE)
    data = models.FileField(storage=ITEM_FSS, upload_to='%Y/%m/%d')
    # thumbnail = models.FileField(storage=ITEM_FSS, upload_to='%Y/%m/%d', null=True, blank=True)
    # parent = models.ForeignKey(Item, null=True, blank=True) # for clones
    hide_after = models.DateTimeField(null=True, blank=True)
    hide_before = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
	ordering = ['-last_modified']

    def save_upload_file(self, f):
	if not self.id:
	    raise Exception, "save_upload_file trying to save a model which has no IID"
	name = str(self.id) + '.' + f.name
	self.data.save(name, f)

##################################################################

class Comment(models.Model, Thing):

    """This is the modelspace representation of the Comment object"""

    key_prefix = "comment"

    title = models.CharField(max_length=settings.MINE_STRINGSIZE)
    body = models.TextField(null=True, blank=True)
    likes = models.BooleanField(default=False)
    item = models.ForeignKey(Item)
    relation = models.ForeignKey(Relation)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
	ordering = ['-id']

##################################################################

class VanityURL(models.Model, Thing):

    """The VanityURL model implements a TinyURL-like concept, allowing
    arbitrary cookies to map to much longer URLs, indexable either by
    'name' or 'index' (suitably compressed)"""

    key_prefix = "vurl"

    name = models.SlugField(max_length=settings.MINE_STRINGSIZE, unique=True)
    link = models.TextField(null=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name='vurls_tagged', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
	ordering = ['-id']
	verbose_name = 'Vanity URL'

##################################################################

class MineRegistry(models.Model):

    """key/value pairs for Mine configuration"""

    key = models.SlugField(max_length=settings.MINE_STRINGSIZE, unique=True)
    value = models.TextField(null=True, blank=True)
    secret = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
	ordering = ['key']
	verbose_name = 'Registry'
	verbose_name_plural = 'Registry'

    def __unicode__(self):
	return self.key

##################################################################
##################################################################
##################################################################


###
# allocate the runtime tables

m2s_table = {}
s2m_table = {}
defer_s2m_table = {}

for prefix in class_prefixes.iterkeys():
    m2s_table[prefix] = {}
    s2m_table[prefix] = {}
    defer_s2m_table[prefix] = {} # s2m stuff that requires a DB entry

###
# populate the runtime tables

for (sattr, mattr, defer, r2s_func, s2m_func, m2s_func) in key_conversion:
    for prefix in class_prefixes.iterkeys():

	if sattr.startswith(prefix):

	    if m2s_func:
		m2s_table[prefix][mattr] = (m2s_func, sattr)

	    if s2m_func:
		t = (r2s_func, s2m_func, mattr)

		if defer:
		    defer_s2m_table[prefix][sattr] = t
		else:
		    s2m_table[prefix][sattr] = t

	    break
    else:
	raise Exception, "unrecognised prefix in key_conversion: " + sattr

###
# convert a model to a structure

def model_to_structure(kind, m):
    s = {}
    for mattr, (m2s_func, sattr) in m2s_table[kind].iteritems():
	m2s_func(m, mattr, s, sattr)
    return s

###
# convert a request to a model

# one of these days i want to convert this to a @classmethod on a
# subclass of Model which I can then use as a parent class of all the
# Models in this file; it would be a lot neater and would bring the
# logic much closer to the Model, ie: something like:
#
# m = Comment.saveRequest(r)
# return foo(m.structure())
#
# ...the saveRequest() and structure() and some other shared methods
# being held in the intermediate class; however that level of
# complexity can wait a while longer -- alec

@transaction.commit_on_success # ie: rollback if it raises an exception
def request_to_model_and_save(kind, r, update_id=None):

    instantiator = class_prefixes[kind] # create the model

    # is this an update?
    if update_id:
	m = instantiator.objects.get(id=update_id)

    else:
	margs = {}
	m = instantiator(**margs)

    # build a shadow structure: useful for debug/clarity
    s = {}

    # for each target attribute
    for sattr, (r2s_func, s2m_func, mattr) in s2m_table[kind].iteritems():

	# is it there?
	if not sattr in r.REQUEST: continue

	# rip the attribute out of the request and convert to python int/str
	r2s_func(r, sattr, s)

	# s2m the value into the appropriate attribute
	s2m_func(s, sattr, m, mattr)

    # save the model
    m.save()

    # do the deferred (post-save) initialisation
    needs_save = False

    # for each deferred target attribute
    for sattr, (r2s_func, s2m_func, mattr) in defer_s2m_table[kind].iteritems():

	# special case file-saving, assume <model>.save_uploaded_file() works
	if sattr in ( 'itemData' ): # ...insert others here...
	    if sattr in r.FILES:
		uf = r.FILES[sattr]
		ct = uf.content_type
		m.save_upload_file(uf)
		needs_save = True

	else:
	    # repeat the above logic
	    if not sattr in r.REQUEST: continue
	    r2s_func(r, sattr, s)
	    s2m_func(s, sattr, m, mattr)
	    needs_save = True

    # update if we did anything
    if needs_save: m.save()

    # return it
    return m

##################################################################
##################################################################
##################################################################
