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

# important stuff for below

# magic storage for database items
item_file_storage = FileSystemStorage(location = settings.MINE_DBDIR_FILES)

# choices for the item status
item_status_choices = (
    ( 'X', 'private' ),
    ( 'S', 'shared' ),
    ( 'P', 'public' ),
    )

# create a reverse lookup table, long->short
# other direction is covered by m.get_status_display()
status_lookup = {} 
for short, long in item_status_choices: status_lookup[long] = short

##################################################################

# The transcoder methods below provide a lot of the security for
# pymine, and govern the movement of data between three 'spaces" of
# data representation; these are:

# r-space - request space, where data are held in a HttpRequest
# s-space - structure space, where data are held in a dict
# m-space - model space, where data are fields in model instances

# The reason for keeping separate spaces is partly philosophic - that
# there should be a clearly defined breakpoint between the two worlds,
# and this is it; if we just serialized models and slung them back and
# forth, the mine would be wedded to Django evermore, which is not a
# good thing;

# If we tried to go the simple route and keep the data structures
# similar, errors would be hard to flush out plus we would tend to do
# things only the Django way - the Mine API was first written from
# scratch and driven using 'curl' so this is definitely portable.

# Further: certain s-space attributes (eg: 'relationInterests') map to
# more than one m-space attributes, so these functions provide parsing
# as well as translation.

# r-space and s-space share exactly the same naming conventions, ie:
# they use mixedCase key (aka: 's-attribute' or 'sattr') such as
# "relationName" and "tagDescription" and "itemId" to label data; the
# only meaningful difference is that in r-space all data are held in
# HttpRequest objects as strings; when pulled into s-space Python
# dictionaries, any data which are integers (eg: itemId) are converted
# to Python integers.

# For obvious reasons it's never necessary to go from s-space to
# r-space; instead data only ever comes *out* of HttpRequests and
# *into* structures, hence there are only r2s_foo methods, and indeed
# only two of those: r2s_string and r2s_int:

def r2s_string(r, rname, s):
    """get rname from HttpRequest r's r.REQUEST and populate structure s with it; assume something else checked existence"""
    s[rname] = r.REQUEST[rname]

def r2s_int(r, rname, s):
    """get rname from HttpRequest r's r.REQUEST and populate structure s with it after converting to int; assume something else checked existence"""
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
    if x: s[sattr] = x

def s2m_copy(s, sattr, m, mattr):
    """Copy sattr from s to mattr in m"""
    if sattr in s: setattr(m, mattr, s[sattr])

# Because a lot of our code is table-driven, it helps to have a couple
# of dummy routines as filler where beneficial:

def m2s_dummy(m, mattr, s, sattr):
    """Barfing Placeholder"""
    raise RuntimeError, 'something invoked m2s_dummy'

def s2m_dummy(s, sattr, m, mattr):
    """Barfing Placeholder"""
    raise RuntimeError, 'something invoked s2m_dummy'

# One of the more complex translations between spaces are DateTime
# objects; in m-space we use whatever Django mandates, and in s-space
# we use a string representation of the time/date in ISO format, which
# is very close to what ATOM specifies - which in turn is probably
# what we will standardise on eventually

def m2s_date(m, mattr, s, sattr):
    """Copy a DateTime from m to a isoformat string in s"""
    x = getattr(m, mattr)
    if x: s[sattr] = x.isoformat()

def s2m_date(s, sattr, m, mattr):
    if sattr in s:
	raise RuntimeError, "not yet integrated the Date parser"

# Specialist Type Conversion - Note: Where we are writing custom
# converters we don't generally bother to use introspection because we
# know the names of the model fields.

# The 'Comment' model has an 'item' field that is a ForeignKey
# representing the item-being-commented-upon; in s-space this is
# represented as the itemId being commented upon, an int.

def m2s_comitem(m, mattr, s, sattr):
    if mattr != 'item' or sattr != 'commentItem':
	raise RuntimeError, "m2s_comitem is confused"
    x = m.item
    if x: s[sattr] = x.id

def s2m_comitem(s, sattr, m, mattr):
    if mattr != 'item' or sattr != 'commentItem':
	raise RuntimeError, "s2m_comitem is confused"
    if sattr in s:
	m.item = Item.objects.get(id=s[sattr]) # ITEM LOOKUP


# The 'Comment' model also has a 'relation' field that is a ForeignKey
# representing the relation-submitting-the-comment; in s-space this is
# represented as the relationName, a string

def m2s_comrel(m, mattr, s, sattr):
    if mattr != 'relation' or sattr != 'commentRelation':
	raise RuntimeError, "m2s_comrel is confused"
    x = m.relation
    if x: s[sattr] = x.name

def s2m_comrel(s, sattr, m, mattr):
    if mattr != 'relation' or sattr != 'commentRelation':
	raise RuntimeError, "s2m_comrel is confused"
    if sattr in s:
	m.relation = Relation.objects.get(name=s[sattr]) # RELATION LOOKUP

# The 'Tag' model contains a ManyToMany field which cites the
# implications / multiple parents that any given Tag can have; in
# s-space this is represented as a space-separated string which
# contatenates tagNames.  Loops are possible, but benign.

def m2s_tagimplies(m, mattr, s, sattr):
    if mattr != 'implies' or sattr != 'tagImplies':
	raise RuntimeError, "m2s_tagimplies is confused"
    x = ' '.join([ x.name for x in m.implies.all() ])
    if x: s[sattr] = x

def s2m_tagimplies(s, sattr, m, mattr):
    if mattr != 'implies' or sattr != 'tagImplies':
	raise RuntimeError, "s2m_tagimplies is confused"
    if sattr in s:
	for x in s[sattr].split():
	    m.implies.add(Tag.objects.get(name=x))

# VirtualURL models contain very basic tagging for reference puproses;
# the model field is 'tags' and is a space-separated string which
# contatenates tagNames.

def m2s_vurltags(m, mattr, s, sattr):
    if mattr != 'tags' or sattr != 'vurlTags':
	raise RuntimeError, "m2s_vurltags is confused"
    x = ' '.join([ x.name for x in m.tags.all() ])
    if x: s[sattr] = x

def s2m_vurltags(s, sattr, m, mattr):
    if mattr != 'tags' or sattr != 'vurlTags':
	raise RuntimeError, "s2m_vurltags is confused"
    if sattr in s:
	for x in s[sattr].split(): m.implies.add(Tag.objects.get(name=x))

# itemStatus is a multi-choice field; the s-space representation of
# itemStatus ('public', 'shared', 'private') must be mapped back and
# forth to the single characters which are held in item.status

def m2s_itemstatus(m, mattr, s, sattr):
    if mattr != 'status' or sattr != 'itemStatus':
	raise RuntimeError, "s2m_itemtags is confused"
    x = m.get_status_display()
    if x: s[sattr] = x

def s2m_itemstatus(s, sattr, m, mattr):
    if mattr != 'status' or sattr != 'itemStatus':
	raise RuntimeError, "m2s_itemtags is confused"
    x = s[sattr]

    if x in status_lookup:
	setattr(m, mattr, status_lookup[x])
    else:
	raise RuntimeError, "s2m_itemstatus cannot remap status: " + x

# itemTags is a complex tagging string: in s-space it is a
# space-separated string like "wine beer for:alice not:bob" where
# 'alice' and 'bob' are relationNames and 'wine' and 'beer' are
# tagNames; that data is parsed out and split into *three* separate
# m-space fields: m.tags, m.item_for_relations, m.item_not_relations -
# which are all ManyToMany fields.

def m2s_itemtags(m, mattr, s, sattr):
    if mattr != 'tags' or sattr != 'itemTags':
	raise RuntimeError, "m2s_itemtags is confused"

    # i like this bit of code
    x = " ".join(x for x in itertools.chain([ i.name for i in m.tags.all() ],
					    [ "for:%s" % i.name for i in m.item_for_relations.all() ],
					    [ "not:%s" % i.name for i in m.item_not_relations.all() ]))
    if x: s[sattr] = x

def s2m_itemtags(s, sattr, m, mattr):
    if mattr != 'tags' or sattr != 'itemTags':
	raise RuntimeError, "s2m_itemtags is confused"
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

def m2s_relints(m, mattr, s, sattr):
    if mattr != 'interests' or sattr != 'relationInterests':
	raise RuntimeError, "m2s_relints is confused"

    x = " ".join(x for x in itertools.chain([ i.name for i in m.tags.all() ],
					    [ "require:%s" % i.name for i in m.tags_required.all() ],
					    [ "exclude:%s" % i.name for i in m.tags_excluded.all() ]))
    if x: s[sattr] = x

def s2m_relints(s, sattr, m, mattr):
    if mattr != 'interests' or sattr != 'relationInterests':
	raise RuntimeError, "s2m_relints is confused"
    if sattr in s:
	for x in s[sattr].split():
	    if x.startswith('require:'): m.tags_required.add(Tag.objects.get(name=x[8:]))
	    elif x.startswith('exclude:'): m.tags_excluded.add(Tag.objects.get(name=x[8:]))
	    elif x.startswith('except:'): m.tags_excluded.add(Tag.objects.get(name=x[7:])) # common typo
	    else: m.tags.add(Tag.objects.get(name=x))

# The Thing class is a base class that exists to provide a few common
# methods to the core Mine models; it's obviously easy to 'get' or
# 'set' the fields of a model instance because you can always do
# "m.field = foo" or something

# What we need to do is:

# 1) get the svalue of a sattr that's associated with some model's
#    corresponding mattr

# 2) empty/nullify the mattr that corresponds with a model's sattr

# 3) create, update or clone a model, from information held in a
#    HttpRequest (r-space)

# 4) return an entire s-structure populated from a model

# Methods are provided below in Thing() to permit the above and then
# are inherited by most of the Mine models; for this to work there
# needs to be a small amount of linker logic to bypass major circular
# dependencies, and that's provided at the end of this file.

class Thing():

    # sattr_prefix will be checked in methods below, inheriting from
    # subclasses of Thing.

    sattr_prefix = 'thing' # subclass should override this for runtime
    id = 42 # fake

    # IMPORTANT: see s_classes registration at the bottom of this
    # file; there *is* slight replication of code but it's unavoidable
    # since this is essentially a linker issue.  For the
    # initialisation of Thing() it ie enough to have the keys in place
    # and then have the registration code populate them for runtime.

    s_classes = {
	'thing': None, # will be populated later
	'comment': None, # will be populated later
	'item': None, # will be populated later
	'relation': None, # will be populated later
	'tag': None, # will be populated later
	'vurl': None, # will be populated later
	}

    # enormous table of things to make and do

    sattr_conversion_table = (
	(  'thingId',                 'id',               False,  r2s_int,     s2m_copy,        m2s_copy,        ),
	(  'commentBody',             'body',             False,  r2s_string,  s2m_copy,        m2s_copy,        ),
	(  'commentCreated',          'created',          False,  r2s_string,  s2m_date,        m2s_date,        ),
	(  'commentId',               'id',               False,  r2s_int,     s2m_copy,        m2s_copy,        ),
	(  'commentItem',             'item',             False,  r2s_int,     s2m_comitem,     m2s_comitem,     ),
	(  'commentLastModified',     'last_modified',    False,  r2s_string,  s2m_date,        m2s_date,        ),
	(  'commentLikes',            'likes',            False,  r2s_string,  s2m_copy,        m2s_copy,        ),
	(  'commentRelation',         'relation',         False,  r2s_string,  s2m_comrel,      m2s_comrel,      ),
	(  'commentTitle',            'title',            False,  r2s_string,  s2m_copy,        m2s_copy,        ),
	(  'itemCreated',             'created',          False,  r2s_string,  s2m_date,        m2s_date,        ),
	(  'itemData',                'data',             True,   None,        s2m_dummy,       None,            ),
	(  'itemDescription',         'description',      False,  r2s_string,  s2m_copy,        m2s_copy,        ),
	(  'itemHideAfter',           'hide_after',       False,  r2s_string,  s2m_date,        m2s_date,        ),
	(  'itemHideBefore',          'hide_before',      False,  r2s_string,  s2m_date,        m2s_date,        ),
	(  'itemId',                  'id',               False,  r2s_int,     s2m_copy,        m2s_copy,        ),
	(  'itemLastModified',        'last_modified',    False,  r2s_string,  s2m_date,        m2s_date,        ),
	(  'itemName',                'name',             False,  r2s_string,  s2m_copy,        m2s_copy,        ),
	(  'itemStatus',              'status',           False,  r2s_string,  s2m_itemstatus,  m2s_itemstatus,  ),
	(  'itemTags',                'tags',             True,   r2s_string,  s2m_itemtags,    m2s_itemtags,    ),
	(  'itemType',                'content_type',     False,  r2s_string,  s2m_copy,        m2s_copy,        ),
	(  'relationCallbackURL',     'url_callback',     False,  r2s_string,  s2m_copy,        m2s_copy,        ),
	(  'relationCreated',         'created',          False,  r2s_string,  s2m_date,        m2s_date,        ),
	(  'relationDescription',     'description',      False,  r2s_string,  s2m_copy,        m2s_copy,        ),
	(  'relationEmailAddress',    'email_address',    False,  r2s_string,  s2m_copy,        m2s_copy,        ),
	(  'relationEmbargoAfter',    'embargo_after',    False,  r2s_string,  s2m_date,        m2s_date,        ),
	(  'relationEmbargoBefore',   'embargo_before',   False,  r2s_string,  s2m_date,        m2s_date,        ),
	(  'relationHomepageURL',     'url_homepage',     False,  r2s_string,  s2m_copy,        m2s_copy,        ),
	(  'relationId',              'id',               False,  r2s_int,     s2m_copy,        m2s_copy,        ),
	(  'relationImageURL',        'url_image',        False,  r2s_string,  s2m_copy,        m2s_copy,        ),
	(  'relationInterests',       'interests',        True,   r2s_string,  s2m_relints,     m2s_relints,     ),
	(  'relationLastModified',    'last_modified',    False,  r2s_string,  s2m_date,        m2s_date,        ),
	(  'relationName',            'name',             False,  r2s_string,  s2m_copy,        m2s_copy,        ),
	(  'relationNetworkPattern',  'network_pattern',  False,  r2s_string,  s2m_copy,        m2s_copy,        ),
	(  'relationVersion',         'version',          False,  r2s_string,  s2m_copy,        m2s_copy,        ),
	(  'tagCreated',              'created',          False,  r2s_string,  s2m_date,        m2s_date,        ),
	(  'tagDescription',          'description',      False,  r2s_string,  s2m_copy,        m2s_copy,        ),
	(  'tagId',                   'id',               False,  r2s_int,     s2m_copy,        m2s_copy,        ),
	(  'tagImplies',              'implies',          True,   r2s_string,  s2m_tagimplies,  m2s_tagimplies,  ),
	(  'tagLastModified',         'last_modified',    False,  r2s_string,  s2m_date,        m2s_date,        ),
	(  'tagName',                 'name',             False,  r2s_string,  s2m_copy,        m2s_copy,        ),
	(  'vurlCreated',             'created',          False,  r2s_string,  s2m_date,        m2s_date,        ),
	(  'vurlId',                  'id',               False,  r2s_int,     s2m_copy,        m2s_copy,        ),
	(  'vurlLastModified',        'last_modified',    False,  r2s_string,  s2m_date,        m2s_date,        ),
	(  'vurlLink',                'link',             False,  r2s_string,  s2m_copy,        m2s_copy,        ),
	(  'vurlName',                'name',             False,  r2s_string,  s2m_copy,        m2s_copy,        ),
	(  'vurlTags',                'tags',             True,   r2s_string,  s2m_vurltags,    m2s_vurltags,    ),
	)

    # A word about deferral: some s2m conversions can only take place
    # after the model has been written to the database; this is
    # because ManyToMany keys (and perhaps other ForeignKeys?) can
    # only be created once a id/primary key has been created for a new
    # entry; therefore some of the translations have been flagged for
    # "deferral", ie: a second round of processing after the first
    # m.save(); this is OK because there is a rollback set up around
    # the model-alteration method in case an exception is thrown.

    # these tables get used to map sattr and marrt names to the tuples
    # of how-to-convert from one to the other.

    m2s_table = {}
    s2m_table = {}
    defer_s2m_table = {}

    # table population; we shall be asking questions later.

    for prefix in s_classes.iterkeys():
	m2s_table[prefix] = {}
	s2m_table[prefix] = {}
	defer_s2m_table[prefix] = {}

    for (sattr, mattr, deferflag, r2s_func, s2m_func, m2s_func) in sattr_conversion_table:
	for prefix in s_classes.iterkeys():
	    if sattr.startswith(prefix):
		if m2s_func:
		    m2s_table[prefix][mattr] = (m2s_func, sattr)
		if s2m_func:
		    t = (r2s_func, s2m_func, mattr)
		    if deferflag:
			defer_s2m_table[prefix][sattr] = t
		    else:
			s2m_table[prefix][sattr] = t
		break # for loop
	else: # for loop; you can have a else: for a for loop in python, how cool!
	    raise RuntimeError, "unrecognised prefix in sattr_conversion: " + sattr

    # update_from_request updates a (possibly blank) instance of a
    # model, with data that comes from a HttpRequest (ie: that is in
    # r-space)

    # it is used as a backend by new_from_request() [which creates a
    # blank model instance, then updates it from the request] *and* by
    # clone_from_request() [which creates a blank Item, clones it from
    # the old one, then updates it from the request]

    @transaction.commit_on_success # <- rollback if it raises an exception
    def update_from_request(self, r, **kwargs):

	# build a shadow structure: useful for debug/clarity
	s = {}

	# for each target attribute
	for sattr, (r2s_func, s2m_func, mattr) in self.s2m_table[self.sattr_prefix].iteritems():

            # first check if it is in the kwargs (override / extra)
            # else rip the attribute out of the request and convert to python int/str
            # else skip
            if sattr in kwargs: s[sattr] = kwargs[sattr]
	    elif sattr in r.REQUEST: r2s_func(r, sattr, s)
            else: continue

	    # s2m the value into the appropriate attribute
	    s2m_func(s, sattr, self, mattr)

	# save the model
	self.save()

	# do the deferred (post-save) initialisation
	needs_save = False

	# for each deferred target attribute
	for sattr, (r2s_func, s2m_func, mattr) in self.defer_s2m_table[self.sattr_prefix].iteritems():

	    # special case file-saving, assume <model>.save_uploaded_file() works
	    if sattr in ( 'itemData' ): # ...insert others here...
		if sattr in r.FILES:
		    uf = r.FILES[sattr]
		    ct = uf.content_type
		    self.save_upload_file(uf)
		    needs_save = True

	    else:
		# repeat the above logic
                if sattr in kwargs: s[sattr] = kwargs[sattr]
                elif sattr in r.REQUEST: r2s_func(r, sattr, s)
                else: continue
		s2m_func(s, sattr, self, mattr)
		needs_save = True

	# update if we did anything
	if needs_save: self.save()

	# return it
	return self

    # cloning an item, as described above

    def clone_from_request(self, r, **kwargs):
	if self.sattr_prefix != 'item':
	    raise RuntimeError, "clone_from_request called on non-item"

	instantiator = self.s_classes[self.sattr_prefix]

	margs = {}

	m = instantiator(**margs)

	### XXX: TBD: clone self to m here
	### XXX: TBD: clone self to m here
	### XXX: TBD: clone self to m here
	### XXX: TBD: clone self to m here
	### XXX: TBD: clone self to m here

	return m.update_from_request(r, **kwargs)

    # creating a new model

    @classmethod # <- new_from_request is an alternative constructor, ergo: classmethod
    def new_from_request(self, r, **kwargs):
	instantiator = self.s_classes[self.sattr_prefix]
	margs = {}
	m = instantiator(**margs)
	return m.update_from_request(r, **kwargs)

    # looking up a mattr from a sattr is tedious since it has to be
    # done in two places; this wraps that for convenience

    def lookup_mattr(self, sattr):
	if sattr in self.s2m_table[self.sattr_prefix][sattr]:
	    t = s2m_table[self.sattr_prefix][sattr]
	elif sattr in self.defer_s2m_table[self.sattr_prefix][sattr]:
	    t = defer_s2m_table[self.sattr_prefix][sattr]
	else:
	    raise RuntimeError, "lookup_mattr cannot lookup: " + sattr
	return t

    # get_sattr and delete_sattr methods: supporting the
    # /api/relation/42/relationName.json and similar methods.

    def get_sattr(self, sattr):
	# check validity of sattr
        if not sattr.startswith(self.sattr_prefix):
            raise RuntimeError, "get_sattr asked to look up bogus sattr: " + sattr

	# lookup equivalent model field
        r2s_func, s2m_func, mattr = lookup_mattr(sattr)

	# retreive equivalent model field
        x = getattr(self, mattr)

        # lookup m2s conversion routine
        m2s_func, sattr2 = m2s_table[self.sattr_prefix][mattr]

        # sanity check
        assert sattr == sattr2, "m2s_table corruption, reverse lookup yielded wrong result"

	# convert to s-form
        s = {}
        m2s_func(self, mattr, s, sattr)

        # return
	return s[sattr]

    @transaction.commit_on_success # <- rollback if it raises an exception
    def delete_sattr(self, sattr):
	# check validity of sattr
        if not sattr.startswith(self.sattr_prefix):
            raise RuntimeError, "get_sattr asked to look up bogus sattr: " + sattr

	# lookup equivalent model field
        r2s_func, s2m_func, mattr = lookup_mattr(sattr)

        # zero that field
        setattr(self, None)

        # try saving
        self.save()

    # render a model into a structure quitable for serializing and
    # returning to the user.

    def to_structure(self):
	s = {}
	for mattr, (m2s_func, sattr) in self.m2s_table[self.sattr_prefix].iteritems():
	    m2s_func(self, mattr, s, sattr)
	return s

##################################################################
##################################################################
##################################################################

class Tag(models.Model, Thing):

    """This is the modelspace representation of the Tag object"""

    sattr_prefix = "tag"

    name = models.SlugField(max_length=settings.MINE_STRINGSIZE, unique=True)
    description = models.TextField(null=True, blank=True)
    implies = models.ManyToManyField('self', symmetrical=False, related_name='x_implies', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
	ordering = ['name']

    def __unicode__(self):
	return self.name

##################################################################

class Relation(models.Model, Thing):

    """This is the modelspace representation of the Relation object"""

    sattr_prefix = "relation"

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

    def __unicode__(self):
	return self.name

##################################################################

class Item(models.Model, Thing):

    """This is the modelspace representation of the Item object"""

    sattr_prefix = "item"
    name = models.CharField(max_length=settings.MINE_STRINGSIZE)
    description = models.TextField(null=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name='items_tagged', null=True, blank=True)
    item_for_relations = models.ManyToManyField(Relation, related_name='items_explicitly_for', null=True, blank=True)
    item_not_relations = models.ManyToManyField(Relation, related_name='items_explicitly_not', null=True, blank=True)
    status = models.CharField(max_length=1, choices=item_status_choices)
    content_type = models.CharField(max_length=settings.MINE_STRINGSIZE)
    data = models.FileField(storage=item_file_storage, upload_to='%Y/%m/%d')
    parent = models.ForeignKey('self', null=True, blank=True) # only set for clones
    hide_after = models.DateTimeField(null=True, blank=True)
    hide_before = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
	ordering = ['-last_modified']

    def __unicode__(self):
	return self.name

    def save_upload_file(self, f):
	if not self.id:
	    raise RuntimeError, "save_upload_file trying to save a model which has no IID"

	name = str(self.id) + '.' + f.name

	self.data.save(name, f)

##################################################################

class Comment(models.Model, Thing):

    """This is the modelspace representation of the Comment object"""

    sattr_prefix = "comment"
    title = models.CharField(max_length=settings.MINE_STRINGSIZE)
    body = models.TextField(null=True, blank=True)
    likes = models.BooleanField(default=False)
    item = models.ForeignKey(Item)
    relation = models.ForeignKey(Relation)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
	return self.title

    class Meta:
	ordering = ['-id']

##################################################################

class VanityURL(models.Model, Thing):

    """The VanityURL model implements a TinyURL-like concept, allowing
    arbitrary cookies to map to much longer URLs, indexable either by
    'name' or 'index' (suitably compressed)"""

    sattr_prefix = "vurl"
    name = models.SlugField(max_length=settings.MINE_STRINGSIZE, unique=True)
    link = models.TextField(null=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name='vurls_tagged', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
	return self.name

    class Meta:
	ordering = ['-id']
	verbose_name = 'Vanity URL'

##################################################################

class MineRegistry(models.Model): # not a Thing

    """key/value pairs for Mine configuration"""

    key = models.SlugField(max_length=settings.MINE_STRINGSIZE, unique=True)
    value = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def to_structure(self):
	s = {}
        s[self.key] = self.value # this is why it is not a Thing
        s['keyCreated'] = m2s_date(self.created)
        s['keyLastModified'] = m2s_date(self.last_modified)
	return s

    class Meta:
	ordering = ['key']
	verbose_name = 'Registry'
	verbose_name_plural = 'Registry'

    def __unicode__(self):
	return self.key

##################################################################

class EventLog(models.Model): # not a Thing

    """key/value pairs for Mine configuration"""

    type = models.SlugField(max_length=settings.MINE_STRINGSIZE)
    action = models.CharField(max_length=settings.MINE_STRINGSIZE, null=False, blank=False)
    # relation = foo
    result = models.CharField(max_length=settings.MINE_STRINGSIZE, null=False, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    # need to store relation

    @classmethod
    def new(self, type, action):
        el = EventLog(type=type, action=action, result="new")
        el.save()

    def update(self, result):
        self.result = result
        self.save()

    def to_structure(self):
	s = {}
        s['eventType'] = self.type
        s['eventAction'] = self.action
        s['eventResult'] = self.result
        s['eventCreated'] = m2s_date(self.created)
        s['eventLastModified'] = m2s_date(self.last_modified)
	return s

    class Meta:
	ordering = ['last_modified']
	verbose_name = 'EventLog'
	verbose_name_plural = 'EventLog'

    def __unicode__(self):
	return self.event

##################################################################

# this is a critical bit of code which registers all thing-classes
# back with the parent thing; key=prefix, value=class

for thing in (Comment, Item, Relation, Tag, VanityURL):
    Thing.s_classes[thing.sattr_prefix] = thing

##################################################################
