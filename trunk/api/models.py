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

import base58

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

class AbstractModelField:
    STRING_SHORT = 256

    @classmethod
    def __defopts(self, **kwargs):
	if kwargs.get('required', True):
	    opts = dict(null=False, blank=False)
	else:
	    opts = dict(null=True, blank=True)

	for foo in ('unique', 'symmetrical'):
	    if foo in kwargs:
		opts[foo] = kwargs[foo]

	return opts

    @classmethod
    def last_modified(self):
	return models.DateTimeField(auto_now=True)

    @classmethod
    def created(self):
	return models.DateTimeField(auto_now_add=True)

    @classmethod
    def datetime(self, **kwargs):
	opts = self.__defopts(**kwargs)
	return models.DateTimeField(**opts)

    @classmethod
    def reference(self, what, **kwargs):
	opts = self.__defopts(**kwargs)
	return models.ForeignKey(what, **opts)

    @classmethod
    def reflist(self, what, **kwargs):
	opts = self.__defopts(**kwargs)
	pivot = kwargs.get('pivot', None)
	if pivot: opts['related_name'] = pivot
	return models.ManyToManyField(what, **opts)

    @classmethod
    def string(self, **kwargs):
	opts = self.__defopts(**kwargs)
	return models.CharField(max_length=self.STRING_SHORT, **opts)

    @classmethod
    def text(self, **kwargs):
	opts = self.__defopts(**kwargs)
	return models.TextField(**opts)

    @classmethod
    def slug(self, **kwargs):
	opts = self.__defopts(**kwargs)
	return models.SlugField(max_length=self.STRING_SHORT, **opts)

    @classmethod
    def bool(self, default):
	return models.BooleanField(default=default)

    @classmethod
    def integer(self, default):
	return models.PositiveIntegerField(default=default)

    @classmethod
    def choice(self, choices):
	return models.CharField(max_length=1, choices=choices)

    @classmethod
    def url(self, **kwargs):
	opts = self.__defopts(**kwargs)
	return models.URLField(max_length=self.STRING_SHORT, **opts)

    @classmethod
    def email(self, **kwargs):
	opts = self.__defopts(**kwargs)
	return models.EmailField(max_length=self.STRING_SHORT, **opts)

    @classmethod
    def file(self, **kwargs):
	return models.FileField(**kwargs) # TODO

##################################################################

class AbstractModel(models.Model):
    created = AbstractModelField.created()
    last_modified = AbstractModelField.last_modified()

    class Meta:
	abstract = True

    @classmethod
    def get_object(self, **kwargs):
	pass

    @classmethod
    def list_objects(self, **kwargs):
	pass

##################################################################

class AbstractXattr(AbstractModel):
    key = AbstractModelField.slug()
    value = AbstractModelField.text()

    class Meta:
	abstract = True

##################################################################

# The transcoder methods below provide a lot of the security for
# pymine, and govern the movement of data between three 'spaces' of
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
# 'relationName' and 'tagDescription' and 'itemId' to label data; the
# only meaningful difference is that in r-space all data are held in
# HttpRequest objects as strings; when pulled into s-space Python
# dictionaries, any data which are integers (eg: itemId) are converted
# to Python integers.

# For obvious reasons it's never necessary to go from s-space to
# r-space; instead data only ever comes *out* of HttpRequests and
# *into* structures, hence there are only r2s_foo methods, and indeed
# only two of those: r2s_string and r2s_int:

##################################################################

def r2s_string(r, rname, s):
    """
    get rname from HttpRequest r's r.POST and populate structure s
    with it; assume something else checked existence
    """

    s[rname] = r.POST[rname]

def r2s_int(r, rname, s):
    """
    get rname from HttpRequest r's r.POST and populate structure s
    with it after converting to int; assume something else checked
    existence in the first place
    """
    s[rname] = int(r.POST[rname])

##################################################################

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

##################################################################

def m2s_copy(m, mattr, s, sattr):
    """Copy mattr from m to sattr in s"""
    x = getattr(m, mattr)
    if x: s[sattr] = x

def s2m_copy(s, sattr, m, mattr):
    """Copy sattr from s to mattr in m"""
    if sattr in s: setattr(m, mattr, s[sattr])

##################################################################

# Because a lot of our code is table-driven, it helps to have a couple
# of dummy routines as filler where beneficial:

def m2s_dummy(m, mattr, s, sattr):
    """Barfing Placeholder"""
    raise RuntimeError, 'something invoked m2s_dummy on %s and %s' % (sattr, mattr)

def s2m_dummy(s, sattr, m, mattr):
    """Barfing Placeholder"""
    raise RuntimeError, 'something invoked s2m_dummy on %s and %s' % (sattr, mattr)

##################################################################

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

##################################################################

# Specialist Type Conversion - Note: Where we are writing custom
# converters we don't generally bother to use introspection because we
# know the names of the model fields.

# The 'Comment' model has an 'item' field that is a ForeignKey
# representing the item-being-commented-upon; in s-space this is
# represented as the itemId being commented upon, an int.

def m2s_comitem(m, mattr, s, sattr):
    if mattr != 'item' or sattr != 'commentItem':
	raise RuntimeError, "m2s_comitem is confused by %s and %s" % (sattr, mattr)
    x = m.item
    if x: s[sattr] = x.id

def s2m_comitem(s, sattr, m, mattr):
    if mattr != 'item' or sattr != 'commentItem':
	raise RuntimeError, "s2m_comitem is confused by %s and %s" % (sattr, mattr)
    if sattr in s:
	m.item = Item.objects.get(id=s[sattr]) # ITEM LOOKUP

##################################################################

# The 'Comment' model also has a 'relation' field that is a ForeignKey
# representing the relation-submitting-the-comment; in s-space this is
# represented as the relationName, a string

def m2s_comrel(m, mattr, s, sattr):
    if mattr != 'relation' or sattr != 'commentRelation':
	raise RuntimeError, "m2s_comrel is confused by %s and %s" % (sattr, mattr)
    x = m.relation
    if x: s[sattr] = x.name

def s2m_comrel(s, sattr, m, mattr):
    if mattr != 'relation' or sattr != 'commentRelation':
	raise RuntimeError, "s2m_comrel is confused by %s and %s" % (sattr, mattr)
    if sattr in s:
	m.relation = Relation.objects.get(name=s[sattr]) # RELATION LOOKUP

##################################################################

# The 'Tag' model contains a ManyToMany field which cites the
# implications / multiple parents that any given Tag can have; in
# s-space this is represented as a space-separated string which
# contatenates tagNames.  Loops are possible, but benign.

def m2s_tagcloud(m, mattr, s, sattr):
    if mattr != 'cloud' or sattr != 'tagCloud':
	raise RuntimeError, "m2s_tagcloud is confused by %s and %s" % (sattr, mattr)
    x = ' '.join([ x.name for x in m.cloud.all() ])
    if x: s[sattr] = x

def m2s_tagimplies(m, mattr, s, sattr):
    if mattr != 'implies' or sattr != 'tagImplies':
	raise RuntimeError, "m2s_tagimplies is confused by %s and %s" % (sattr, mattr)
    x = ' '.join([ x.name for x in m.implies.all() ])
    if x: s[sattr] = x

def s2m_tagimplies(s, sattr, m, mattr):
    if mattr != 'implies' or sattr != 'tagImplies':
	raise RuntimeError, "s2m_tagimplies is confused by %s and %s" % (sattr, mattr)
    if sattr in s:
        m.implies.clear()
	for x in s[sattr].split():
	    m.implies.add(Tag.objects.get(name=x))

##################################################################

# itemStatus is a multi-choice field; the s-space representation of
# itemStatus ('public', 'shared', 'private') must be mapped back and
# forth to the single characters which are held in item.status

def m2s_itemstatus(m, mattr, s, sattr):
    if mattr != 'status' or sattr != 'itemStatus':
	raise RuntimeError, "s2m_itemtags is confused by %s and %s" % (sattr, mattr)
    x = m.get_status_display()
    if x: s[sattr] = x

def s2m_itemstatus(s, sattr, m, mattr):
    if mattr != 'status' or sattr != 'itemStatus':
	raise RuntimeError, "m2s_itemtags is confused by %s and %s" % (sattr, mattr)
    x = s[sattr]

    if x in status_lookup:
	setattr(m, mattr, status_lookup[x])
    else:
	raise RuntimeError, "s2m_itemstatus cannot remap status %s for %s and %s" % (x, sattr, mattr)

##################################################################

# itemTags is a complex tagging string: in s-space it is a
# space-separated string like "wine beer for:alice not:bob" where
# 'alice' and 'bob' are relationNames and 'wine' and 'beer' are
# tagNames; that data is parsed out and split into *three* separate
# m-space fields: m.tags, m.item_for_relations, m.item_not_relations -
# which are all ManyToMany fields.

def m2s_itemtags(m, mattr, s, sattr):
    if mattr != 'tags' or sattr != 'itemTags':
	raise RuntimeError, "m2s_itemtags is confused by %s and %s" % (sattr, mattr)

    # i like this bit of code
    x = " ".join(x for x in itertools.chain([ i.name for i in m.tags.all() ],
					    [ "for:%s" % i.name for i in m.item_for_relations.all() ],
					    [ "not:%s" % i.name for i in m.item_not_relations.all() ]))
    if x: s[sattr] = x

def s2m_itemtags(s, sattr, m, mattr):
    if mattr != 'tags' or sattr != 'itemTags':
	raise RuntimeError, "s2m_itemtags is confused by %s and %s" % (sattr, mattr)
    if sattr in s:
        m.tags.clear()
        m.item_for_relations.clear()
        m.item_not_relations.clear()
	for x in s[sattr].split():
	    if x.startswith('for:'): m.item_for_relations.add(Tag.objects.get(name=x[4:]))
	    elif x.startswith('not:'): m.item_not_relations.add(Tag.objects.get(name=x[4:]))
	    else: m.tags.add(Tag.objects.get(name=x))

##################################################################

# relationInterests is another complex string: in s-space it is a
# space-separated string like "wine require:australia exclude:merlot"
# - the goal of which I hope is fairly clear, that a relation will
# take anything implicitly or explicitly tagged 'wine' but requires
# the 'australia' tag to be also present, rejecting anything that also
# includes the 'merlot' tag; in m-space this also breaks out into
# three fields: m.tags, m.tags_required, m.tags_excluded

def m2s_relints(m, mattr, s, sattr):
    if mattr != 'interests' or sattr != 'relationInterests':
	raise RuntimeError, "m2s_relints is confused by %s and %s" % (sattr, mattr)

    x = " ".join(x for x in itertools.chain([ i.name for i in m.tags.all() ],
					    [ "require:%s" % i.name for i in m.tags_required.all() ],
					    [ "exclude:%s" % i.name for i in m.tags_excluded.all() ]))
    if x: s[sattr] = x

def s2m_relints(s, sattr, m, mattr):
    if mattr != 'interests' or sattr != 'relationInterests':
	raise RuntimeError, "s2m_relints is confused by %s and %s" % (sattr, mattr)
    if sattr in s:
        m.tags.clear()
        m.tags_required.clear()
        m.tags_excluded.clear()
	for x in s[sattr].split():
	    if x.startswith('require:'): m.tags_required.add(Tag.objects.get(name=x[8:]))
	    elif x.startswith('exclude:'): m.tags_excluded.add(Tag.objects.get(name=x[8:]))
	    elif x.startswith('except:'): m.tags_excluded.add(Tag.objects.get(name=x[7:])) # common typo
	    else: m.tags.add(Tag.objects.get(name=x))

##################################################################

# The AbstractThing class is a base model class that exists to provide
# a few common methods to the core Mine models; it's obviously easy to
# 'get' or 'set' the fields of a model instance because you can always
# do "m.field = foo" or something

# What we need to do is:

# 1) get the svalue of a sattr that's associated with some model's
#    corresponding mattr

# 2) empty/nullify the mattr that corresponds with a model's sattr

# 3) create or update, from information held in a HttpRequest (r-space)

# 4) return an entire s-structure populated from a model

# Methods are provided below in Thing() to permit the above and then
# are inherited by most of the Mine models; for this to work there
# needs to be a small amount of linker logic to bypass major circular
# dependencies, and that's provided at the end of this file.

##################################################################

class AbstractThing(AbstractModel):

    # continuing the chain of inheritance
    class Meta:
	abstract = True

    # all these will be overridden in subclasses
    id = -1
    sattr_prefix = None
    xattr_prefix = None
    xattr_manager = None

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

    # enormous table of things to make and do; don't worry about
    # linear lookup overhead because this table gets compiled into
    # dictionaries for fast lookup...

    sattr_conversion_table = (
(  'commentBody',             'body',             False,  r2s_string,  s2m_copy,        m2s_copy,        ),
(  'commentCreated',          'created',          False,  None,        None,            m2s_date,        ),
(  'commentId',               'id',               False,  r2s_int,     s2m_copy,        m2s_copy,        ),
(  'commentItem',             'item',             False,  r2s_int,     s2m_comitem,     m2s_comitem,     ),
(  'commentLastModified',     'last_modified',    False,  None,        None,            m2s_date,        ),
(  'commentRelation',         'relation',         False,  r2s_string,  s2m_comrel,      m2s_comrel,      ),
(  'commentTitle',            'title',            False,  r2s_string,  s2m_copy,        m2s_copy,        ),
(  'itemCreated',             'created',          False,  None,        None,            m2s_date,        ),
(  'itemData',                'data',             True,   None,        None,            None,            ),
(  'itemDescription',         'description',      False,  r2s_string,  s2m_copy,        m2s_copy,        ),
(  'itemHideAfter',           'hide_after',       False,  r2s_string,  s2m_date,        m2s_date,        ),
(  'itemHideBefore',          'hide_before',      False,  r2s_string,  s2m_date,        m2s_date,        ),
(  'itemId',                  'id',               False,  r2s_int,     s2m_copy,        m2s_copy,        ),
(  'itemLastModified',        'last_modified',    False,  None,        None,            m2s_date,        ),
(  'itemName',                'name',             False,  r2s_string,  s2m_copy,        m2s_copy,        ),
(  'itemStatus',              'status',           False,  r2s_string,  s2m_itemstatus,  m2s_itemstatus,  ),
(  'itemTags',                'tags',             True,   r2s_string,  s2m_itemtags,    m2s_itemtags,    ),
(  'itemType',                'content_type',     False,  r2s_string,  s2m_copy,        m2s_copy,        ),
(  'relationCreated',         'created',          False,  None,        None,            m2s_date,        ),
(  'relationDescription',     'description',      False,  r2s_string,  s2m_copy,        m2s_copy,        ),
(  'relationEmbargoAfter',    'embargo_after',    False,  r2s_string,  s2m_date,        m2s_date,        ),
(  'relationEmbargoBefore',   'embargo_before',   False,  r2s_string,  s2m_date,        m2s_date,        ),
(  'relationId',              'id',               False,  r2s_int,     s2m_copy,        m2s_copy,        ),
(  'relationInterests',       'interests',        True,   r2s_string,  s2m_relints,     m2s_relints,     ),
(  'relationLastModified',    'last_modified',    False,  None,        None,            m2s_date,        ),
(  'relationName',            'name',             False,  r2s_string,  s2m_copy,        m2s_copy,        ),
(  'relationNetworkPattern',  'network_pattern',  False,  r2s_string,  s2m_copy,        m2s_copy,        ),
(  'relationVersion',         'version',          False,  r2s_string,  s2m_copy,        m2s_copy,        ),
(  'tagCreated',              'created',          False,  None,        None,            m2s_date,        ),
(  'tagDescription',          'description',      False,  r2s_string,  s2m_copy,        m2s_copy,        ),
(  'tagId',                   'id',               False,  r2s_int,     s2m_copy,        m2s_copy,        ),
(  'tagCloud',                'cloud',            True,   None,        None,            m2s_tagcloud,    ),
(  'tagImplies',              'implies',          True,   r2s_string,  s2m_tagimplies,  m2s_tagimplies,  ),
(  'tagLastModified',         'last_modified',    False,  None,        None,            m2s_date,        ),
(  'tagName',                 'name',             False,  r2s_string,  s2m_copy,        m2s_copy,        ),
(  'thingId',                 'id',               False,  r2s_int,     s2m_copy,        m2s_copy,        ),
(  'vurlCreated',             'created',          False,  None,        None,            m2s_date,        ),
(  'vurlId',                  'id',               False,  r2s_int,     s2m_copy,        m2s_copy,        ),
(  'vurlLastModified',        'last_modified',    False,  None,        None,            m2s_date,        ),
(  'vurlLink',                'link',             False,  r2s_string,  s2m_copy,        m2s_copy,        ),
(  'vurlName',                'name',             False,  r2s_string,  s2m_copy,        m2s_copy,        ),
)

    # A word about deferral: some s2m conversions can only take place
    # after the model has been written to the database; this is
    # because ManyToMany keys (and perhaps other ForeignKeys?) can
    # only be created once a id/primary key has been created for a new
    # entry; therefore some of the translations have been flagged for
    # "deferral", ie: a second round of processing after the first
    # m.save(); this is OK because there is a rollback set up around
    # the model-alteration method in case an exception is thrown.

    # these tables get used to map sattr and mattr names to the tuples
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
	    elif sattr in r.POST: r2s_func(r, sattr, s)
	    else: continue

	    # s2m the value into the appropriate attribute
	    s2m_func(s, sattr, self, mattr)

	# save the model
	self.save() # -> creates an id if there was not one before

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
		elif sattr in r.POST: r2s_func(r, sattr, s)
		else: continue
		s2m_func(s, sattr, self, mattr)
		needs_save = True

        # xattr processing: grab the manager
        mgr = getattr(self, self.xattr_manager)

        # scan the request environment for xattrs
        for k, v in r.POST.iteritems():

            # is it an xattr?
            if not k.startswith(self.xattr_prefix): 
                continue

            # chop out the suffix
            k = k[len(self.xattr_prefix):]

            # get/create the xattr
            xa, created = mgr.get_or_create(key=k, defaults={'value': v})
            if not created: # then it needs updating
                xa.value = v
                xa.save()

            # mark updates on the item
            #needs_save = True

	# update if we did anything
	if needs_save: 
            self.save()

	# return it
	return self

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
	if sattr in self.s2m_table[self.sattr_prefix]:
	    t = self.s2m_table[self.sattr_prefix][sattr]
	elif sattr in self.defer_s2m_table[self.sattr_prefix]:
	    t = self.defer_s2m_table[self.sattr_prefix][sattr]
	else:
	    raise RuntimeError, "lookup_mattr cannot lookup: " + sattr
	return t

    # get_sattr and delete_sattr methods: supporting
    # /api/relation/42/relationName.json and similar methods.

    def get_sattr(self, sattr):
	if sattr.startswith(self.xattr_prefix):
            # chop out the suffix
            k = sattr[len(self.xattr_prefix):]
            # grab the manager
            mgr = getattr(self, self.xattr_manager)
            # lookup the xattr and return it
            xa = mgr.get(key=k)
            return xa.value

	# check validity of sattr
	elif sattr.startswith(self.sattr_prefix):
            # lookup equivalent model field
            r2s_func, s2m_func, mattr = self.lookup_mattr(sattr)
            # retreive equivalent model field
            x = getattr(self, mattr)
            # lookup m2s conversion routine
            m2s_func, sattr2 = m2s_table[self.sattr_prefix][mattr]
            # sanity check
            assert sattr == sattr2, "m2s_table corruption, reverse lookup yielded wrong result"
            # convert to s-form and return
            s = {}
            m2s_func(self, mattr, s, sattr)
            return s[sattr]

        else:
	    raise RuntimeError, "get_sattr asked to look up bogus sattr: " + sattr

    @transaction.commit_on_success # <- rollback if it raises an exception
    def delete_sattr(self, sattr):
	if sattr.startswith(self.xattr_prefix):
            # lookup equivalent model field
            k = sattr[len(self.xattr_prefix):]
            # grab the manager
            mgr = getattr(self, self.xattr_manager)
            # lookup the xattr and delete it
            xa = mgr.get(key=k)
            xa.delete()

	elif sattr.startswith(self.sattr_prefix):
            # lookup equivalent model field
            r2s_func, s2m_func, mattr = self.lookup_mattr(sattr)
            # zero that field
            setattr(self, sattr, None) ############## FIX THIS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            raise RuntimeException, "this method of deletion does not work" 
            # try saving and hope model will bitch if something is wrong
            self.save()

        else:
            raise RuntimeError, "get_sattr asked to look up bogus sattr: " + sattr

    # render a model into a structure suitable for serializing and
    # returning to the user.

    def to_structure(self):
	s = {}

	for mattr, (m2s_func, sattr) in self.m2s_table[self.sattr_prefix].iteritems():
	    m2s_func(self, mattr, s, sattr)

        mgr = getattr(self, self.xattr_manager)

        for xa in mgr.all(): 
            k = '%s%s' % (self.xattr_prefix, xa.key)
            v = xa.value
            s[k] = v

	return s

##################################################################
##################################################################
##################################################################

class LogEvent(AbstractModel):
    """key/value pairs for Mine configuration"""

    logevent_status_choices = (
	( 'o', 'open' ),
	( 'u', 'updated' ),
	( 'c', 'closed' ),
	( 'e', 'error' ),
	( 'm', 'message' ),
	( 'f', 'fatal' ),
	( 'x', 'corrupted' ),
	)

    status = AbstractModelField.choice(logevent_status_choices)
    type = AbstractModelField.string(required=False)
    msg = AbstractModelField.text(required=False)
    ip = AbstractModelField.string(required=False)
    method = AbstractModelField.string(required=False)
    path = AbstractModelField.string(required=False)
    key = AbstractModelField.string(required=False)

    # various faux-constructors that do not return the object

    @classmethod
    def __selfcontained(self, status, type, *args, **kwargs):
	m = " ".join(args)
	el = LogEvent(status=status, type=type, msg=m, **kwargs)
	el.save()

    @classmethod
    def message(self, type, *args, **kwargs):
	self.__selfcontained('m', type, *args, **kwargs)

    @classmethod
    def error(self, type, *args, **kwargs):
	self.__selfcontained('e', type, *args, **kwargs)

    @classmethod
    def fatal(self, type, *args, **kwargs):
	self.__selfcontained('f', type, *args, **kwargs)
	raise RuntimeError, self.msg # set as side effect

    # next three work together; open-update-close/_error

    @classmethod
    def open(self, type, **kwargs):
	el = LogEvent(status='o', type=type, **kwargs)
	el.save()
	return el

    def update(self, *args):
	self.msg = " ".join(args)
	self.status = 'u'
	self.save()

    def __close_status(self, status, *args):
	if self.status in 'ou': # legitimate to close
	    self.msg = " ".join(args)
	    self.status = status
	else: # risk of infinite recursion if exception thrown
	    # leave msg alone
	    self.status = 'x'
	self.save()

    def close(self, *args):
	self.__close_status('c', *args)

    def close_error(self, *args):
	self.__close_status('e', *args)

    def to_structure(self):
	s = {}
	s['eventStatus'] = self.status
	if self.type: s['eventType'] = self.type
	if self.msg: s['eventMessage'] = self.msg
	if self.ip: s['eventIPAddress'] = self.ip
	if self.method: s['eventMethod'] = self.method
	if self.path: s['eventPath'] = self.path
	if self.key: s['eventKey'] = self.key
	s['eventCreated'] = m2s_date(self.created)
	s['eventLastModified'] = m2s_date(self.last_modified)
	return s

    class Meta:
	ordering = ['-last_modified']
	verbose_name = 'Event'

    def __unicode__(self):
	return self.get_status_display()

##################################################################

class Registry(AbstractModel):
    """key/value pairs for Mine configuration"""

    key = AbstractModelField.slug(unique=True)
    value = AbstractModelField.text()

    def to_structure(self):
	s = {}
	s[self.key] = self.value # this is why it is not a Thing
	s['keyCreated'] = self.created.isoformat()
	s['keyLastModified'] = self.last_modified.isoformat()
	return s

    class Meta:
	ordering = ['key']
	verbose_name = 'RegisterEntry'
	verbose_name_plural = 'Registry'

    def __unicode__(self):
	return self.key

##################################################################

class TagXattr(AbstractXattr):
    """tag extended attributes"""

    tag = AbstractModelField.reference('Tag')

    class Meta:
	ordering = ['key']
	# order_with_respect_to = 'tag'
	unique_together = ('tag', 'key')
	verbose_name = 'TagXattr'

    def __unicode__(self):
	return self.key

class Tag(AbstractThing):
    """This is the modelspace representation of the Tag object"""

    sattr_prefix = "tag"

    name = AbstractModelField.slug(unique=True)
    description = AbstractModelField.text(required=False)
    implies = AbstractModelField.reflist('self', symmetrical=False, pivot='implied_by', required=False)
    cloud = AbstractModelField.reflist('self', symmetrical=False, pivot='clouded_by', required=False)

    class Meta:
	ordering = ['name']

    def __unicode__(self):
	return self.name

    def __update_cloud_field(self):
        self.cloud.clear()

        tmap = { self: False }
        loop = True # get us into the processing loop

        while loop:
            loop = False

            for tag, tag_done in tmap.items():
                if tag_done: 
                    continue

                for parent in tag.implies.all():
                    if not tmap.get(parent, False):
                        tmap[parent] = False
                        loop = True

                print "%s is clouding %s" % (self.name, tag.name)
                self.cloud.add(tag)
                tmap[tag] = True

        self.save() # needed?


    def __update_cloud_map(self, tmap):
        """
        I could try ripping out the list of tags just once (avoiding
        ~n! database hits) and reconstructing the map from that, but
        if they change on disk underneath me then something nasty can
        happen; better to let caching at a lower level take the hit...
        """

        # update all the tags with this data
        for tag in tmap.keys():
            tag = Tag.objects.get(id=tag.id) # potentially dirty, reload
            tag.__update_cloud_field()

    def __expand_cloud_map(self):
        """
        This is brute-force and ignorance code but it is proof against loops.
        """

        tmap = { self: False }

        if not self.id:
            return tmap # we are not yet in the database

        loop = True # get us into the processing loop

        while loop:
            loop = False

            for tag, tag_done in tmap.items():
                if tag_done: 
                    continue

                for parent in tag.implies.all():
                    if not tmap.get(parent, False):
                        tmap[parent] = False
                        loop = True

                for child in tag.implied_by.all():
                    if not tmap.get(child, False):
                        tmap[child] = False
                        loop = True

                tmap[tag] = True

        return tmap


    @transaction.commit_on_success # <- rollback if it raises an exception
    def delete_sattr(self, sattr):
        """
        This method overrides AbstractThing.delete_sattr() and acts as
        a hook to detect changes in the Tag implications that might
        trigger a recalculation of the Tag cloud.
        """

        if sattr == 'tagImplies': 
            tmap = self.__expand_cloud_map()
        else:
            tmap = None

        super(Tag, self).delete_sattr(sattr)

        if tmap:
            self.__update_cloud_map(tmap)


    @transaction.commit_on_success # <- rollback if it raises an exception
    def update_from_request(self, r, **kwargs):
        """
        This method overrides AbstractThing.update_from_request() and
        acts as a hook to detect changes in the Tag implications that
        might trigger a recalculation of the Tag cloud.
        """

        if 'tagImplies' in r.REQUEST: 
            tmap = self.__expand_cloud_map()
        else:
            tmap = None

        retval = super(Tag, self).update_from_request(r, **kwargs)

        if tmap:
            self.__update_cloud_map(tmap)
            retval = Tag.objects.get(id=retval.id) # reload, possibly dirty

        return retval

##################################################################

class RelationXattr(AbstractXattr):
    """relation extended attributes"""

    relation = AbstractModelField.reference('Relation')

    class Meta:
	ordering = ['key']
	# order_with_respect_to = 'relation'
	unique_together = ('relation', 'key')
	verbose_name = 'RelationXattr'

    def __unicode__(self):
	return self.key

class Relation(AbstractThing):
    """This is the modelspace representation of the Relation object"""

    sattr_prefix = "relation"

    name = AbstractModelField.slug(unique=True)
    version = AbstractModelField.integer(1)
    description = AbstractModelField.text(required=False)
    embargo_after = AbstractModelField.datetime(required=False)
    embargo_before = AbstractModelField.datetime(required=False)
    network_pattern = AbstractModelField.string(required=False)
    tags = AbstractModelField.reflist(Tag, pivot='relations_with_tag', required=False)
    tags_excluded = AbstractModelField.reflist(Tag, pivot='relations_excluding', required=False)
    tags_required = AbstractModelField.reflist(Tag, pivot='relations_requiring', required=False)

    class Meta:
	ordering = ['name']

    def __unicode__(self):
	return self.name

##################################################################

class ItemXattr(AbstractXattr):
    """item extended attributes"""

    item = AbstractModelField.reference('Item')

    class Meta:
	ordering = ['key']
	# order_with_respect_to = 'item'
	unique_together = ('item', 'key')
	verbose_name = 'ItemXattr'

    def __unicode__(self):
	return self.key

class Item(AbstractThing):
    """This is the modelspace representation of the Item object"""

    sattr_prefix = "item"

    name = AbstractModelField.string()
    content_type = AbstractModelField.string()
    data = AbstractModelField.file(storage=item_file_storage, upload_to='%Y/%m/%d')
    description = AbstractModelField.text(required=False)
    hide_after = AbstractModelField.datetime(required=False)
    hide_before = AbstractModelField.datetime(required=False)
    item_for_relations = AbstractModelField.reflist(Relation, pivot='items_explicitly_for', required=False)
    item_not_relations = AbstractModelField.reflist(Relation, pivot='items_explicitly_not', required=False)
    parent = AbstractModelField.reference('self', required=False) # only set for clones
    status = AbstractModelField.choice(item_status_choices)
    tags = AbstractModelField.reflist(Tag, pivot='items_tagged', required=False)

    class Meta:
	ordering = ['-last_modified']

    def __unicode__(self):
	return self.name

    # cloning an item, as described above

    def clone_from_request(self, r, **kwargs):
	if self.sattr_prefix != 'item':
	    raise RuntimeError, "clone_from_request called on non-item"

	instantiator = self.s_classes[self.sattr_prefix]

	margs = {}

	m = instantiator(**margs)

	### XXX: TBD: clone self to m here

	return m.update_from_request(r, **kwargs)

    def save_upload_file(self, f):
	if not self.id:
	    raise RuntimeError, "save_upload_file trying to save a model which has no IID"
	name = str(self.id) + '.' + f.name
	self.data.save(name, f)

##################################################################

class CommentXattr(AbstractXattr):
    """comment extended attributes"""

    comment = AbstractModelField.reference('Comment')

    class Meta:
	ordering = ['key']
	# order_with_respect_to = 'comment'
	unique_together = ('comment', 'key')
	verbose_name = 'CommentXattr'

    def __unicode__(self):
	return self.key

class Comment(AbstractThing):
    """This is the modelspace representation of the Comment object"""

    sattr_prefix = "comment"

    title = AbstractModelField.string()
    body = AbstractModelField.text(required=False)
    item = AbstractModelField.reference(Item, required=False) # required=False to permit comments on feed where IID=0
    relation = AbstractModelField.reference(Relation)

    def __unicode__(self):
	return self.title

    class Meta:
	ordering = ['-id']

##################################################################

class VurlXattr(AbstractXattr):
    """vurl extended attributes"""

    vurl = AbstractModelField.reference('Vurl')

    class Meta:
	ordering = ['key']
	# order_with_respect_to = 'vurl'
	unique_together = ('vurl', 'key')
	verbose_name = 'VurlXattr'

    def __unicode__(self):
	return self.key

class Vurl(AbstractThing):

    """The Vurl (VanityURL) model implements a TinyURL-like concept,
    allowing arbitrary cookies to map to much longer URLs, indexable
    either by 'name' or 'index' (suitably compressed) ; it also
    provides for much elective, longer token names to be used"""

    sattr_prefix = "vurl"

    name = AbstractModelField.slug(unique=True)
    link = AbstractModelField.text(unique=True) # TODO: does 'unique' work on this?

    def __unicode__(self):
	return self.name

    class Meta:
	ordering = ['-id']

    def vurlkey():
        return base58.b58encode(self.id)

    @classmethod
    def get_with_vurlkey(encoded):
        return Vurl.objects.get(id=base58.b58decode(encoded))

##################################################################
##################################################################
##################################################################

# this is a critical bit of code which registers all thing-classes
# back with the parent AbstractThing class, and populates the other
# Thing-specific fields...

for thing in (Comment, Item, Relation, Tag, Vurl):
    AbstractThing.s_classes[thing.sattr_prefix] = thing
    thing.xattr_prefix = '__' + thing.sattr_prefix
    thing.xattr_manager = thing.sattr_prefix + 'xattr_set'

##################################################################
##################################################################
##################################################################
