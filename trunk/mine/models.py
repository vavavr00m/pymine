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

status_lookup = {}

##################################################################

class Tag(models.Model):

    """This is the modelspace representation of the Tag object"""

    name = models.SlugField(max_length=settings.MINE_STRINGSIZE, unique=True)
    description = models.TextField(null=True, blank=True)
    implies = models.ManyToManyField('self', symmetrical=False, related_name='x_implies', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
	ordering = ['name']

    def __unicode__(self):
	return self.name

    def structure(self):
	return model_to_structure('tag', self)

##################################################################

class Relation(models.Model):

    """This is the modelspace representation of the Relation object"""

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

    def structure(self):
	return model_to_structure('relation', self)

##################################################################

class Item(models.Model):

    """This is the modelspace representation of the Item object"""

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
    hide_after = models.DateTimeField(null=True, blank=True)
    hide_before = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
	ordering = ['-last_modified']

    def __unicode__(self):
	return self.name

    def structure(self):
	return model_to_structure('item', self)

    def save_upload_file(self, f):
        if not self.id:
            raise Exception, "save_upload_file trying to save a model which has no IID"
        name = str(self.id) + '.' + f.name
        self.data.save(name, f)

##################################################################

class Comment(models.Model):

    """This is the modelspace representation of the Comment object"""

    title = models.CharField(max_length=settings.MINE_STRINGSIZE)
    body = models.TextField(null=True, blank=True)
    likes = models.BooleanField(default=False)
    item = models.ForeignKey(Item)
    relation = models.ForeignKey(Relation)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
	ordering = ['-id']

    def __unicode__(self):
	return self.title

    def structure(self):
	return model_to_structure('comment', self)

##################################################################

class VanityURL(models.Model):

    """The VanityURL model implements a TinyURL-like concept, allowing
    arbitrary cookies to map to much longer URLs, indexable either by
    'name' or 'index' (suitably compressed)"""

    name = models.SlugField(max_length=settings.MINE_STRINGSIZE, unique=True)
    link = models.TextField(null=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name='vurls_tagged', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
	ordering = ['-id']
	verbose_name = 'Vanity URL'

    def __unicode__(self):
	return self.name

    def structure(self):
	return model_to_structure('vurl', self)

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

# The transcoder methods below provide a lot of the security for
# pymine; it convert between 'client-space' structural
# s-representations of data as (approximately) specified in the
# protomine API, and the Django-space model-based m-representations;
# the reason for doing this is partly philosophic - that there should
# be a clearly defined breakpoint between the two worlds, and this is
# it; if we just serialized models and slung them back and forth, the
# mine would be wedded to Django evermore, which is not a good thing.
# Also certain s-space attributes (eg: 'relationInterests') map to
# more than one m-space attributes, so these methods provide
# translation.

###
# specialist type conversion

def m2s_commentitem(m, mattr, s, sattr):
    if mattr != 'item' or sattr != 'commentItem': raise Exception, "m2s_commentitem is confused"
    x = m.item
    if x: s[sattr] = x.id

def s2m_commentitem(s, sattr, m, mattr):
    if mattr != 'item' or sattr != 'commentRelation': raise Exception, "s2m_commentitem is confused"
    if sattr in s: m.item = Item.get(id=s[sattr])

###

def m2s_commentrelation(m, mattr, s, sattr):
    if mattr != 'relation' or sattr != 'commentRelation': raise Exception, "m2s_commentrelation is confused"
    x = m.relation
    if x: s[sattr] = x.name

def s2m_commentrelation(s, sattr, m, mattr):
    if mattr != 'relation' or sattr != 'commentRelation': raise Exception, "s2m_commentrelation is confused"
    if sattr in s: m.relation = Relation.get(id=s[sattr])


###

def m2s_tagimplies(m, mattr, s, sattr):
    if mattr != 'implies' or sattr != 'tagImplies': raise Exception, "m2s_tagimplies is confused"
    x = ' '.join([ x.name for x in m.implies.all() ])
    if x: s[sattr] = x


def s2m_tagimplies(s, sattr, m, mattr):
    if mattr != 'implies' or sattr != 'tagImplies': raise Exception, "s2m_tagimplies is confused"
    if sattr in s: 
        for x in s[sattr].split(): m.implies.add(Tag.objects.get(name=x))

###

def m2s_vurltags(m, mattr, s, sattr):
    if mattr != 'tags' or sattr != 'vurlTags': raise Exception, "m2s_vurltags is confused"
    x = ' '.join([ x.name for x in m.tags.all() ])
    if x: s[sattr] = x

def s2m_vurltags(s, sattr, m, mattr):
    if mattr != 'tags' or sattr != 'vurlTags': raise Exception, "s2m_vurltags is confused"
    if sattr in s: 
        for x in s[sattr].split(): m.implies.add(Tag.objects.get(name=x))

###

def m2s_itemstatus(m, mattr, s, sattr):
    if mattr != 'status' or sattr != 'itemStatus': raise Exception, "s2m_itemtags is confused"
    s[sattr] = m.get_status_display()

def s2m_itemstatus(s, sattr, m, mattr):
    if mattr != 'status' or sattr != 'itemStatus': raise Exception, "m2s_itemtags is confused"
    x = s[sattr]
    if x in status_lookup: 
        setattr(m, mattr, status_lookup[x])
    else:
        raise Exception, "s2m_itemstatus cannot remap status: " + x

###

def m2s_itemtags(m, mattr, s, sattr):
    if mattr != 'tags' or sattr != 'itemTags': raise Exception, "m2s_itemtags is confused"

    x = " ".join(x for x in itertools.chain([ i.name for i in m.tags.all() ],
					    [ "for:%s" % i.name for i in m.item_for_relations.all() ],
					    [ "not:%s" % i.name for i in m.item_not_relations.all() ]))
    if x: s[sattr] = x

def s2m_itemtags(s, sattr, m, mattr):
    if mattr != 'tags' or sattr != 'itemTags': raise Exception, "s2m_itemtags is confused"
    if sattr in s: 
        for x in s[sattr].split(): 
            if x.startswith('for:'): m.item_for_relations.add(Tag.objects.get(name=x[4:]))
            elif x.startswith('not:'): m.item_not_relations.add(Tag.objects.get(name=x[4:]))
            else: m.tags.add(Tag.objects.get(name=x))


###

def m2s_relationinterests(m, mattr, s, sattr):
    if mattr != 'interests' or sattr != 'relationInterests': raise Exception, "m2s_relationinterests is confused"

    x = " ".join(x for x in itertools.chain([ i.name for i in m.tags.all() ],
					    [ "require:%s" % i.name for i in m.tags_required.all() ],
					    [ "exclude:%s" % i.name for i in m.tags_excluded.all() ]))
    if x: s[sattr] = x

def s2m_relationinterests(s, sattr, m, mattr):
    if mattr != 'interests' or sattr != 'relationInterests': raise Exception, "s2m_relationinterests is confused"
    if sattr in s: 
        for x in s[sattr].split(): 
            if x.startswith('require:'): m.tags_required.add(Tag.objects.get(name=x[8:]))
            elif x.startswith('exclude:'): m.tags_excluded.add(Tag.objects.get(name=x[8:]))
            elif x.startswith('except:'): m.tags_excluded.add(Tag.objects.get(name=x[7:])) # common typo
            else: m.tags.add(Tag.objects.get(name=x))

###
# int type conversion

def m2s_int(m, mattr, s, sattr):
    x = getattr(m, mattr)
    if x is not None: s[sattr] = x

def s2m_int(s, sattr, m, mattr):
    if sattr in s: 
        setattr(m, mattr, s[sattr])

###
# string type conversion

def m2s_string(m, mattr, s, sattr):
    x = getattr(m, mattr)
    if x is not None: s[sattr] = x

def s2m_string(s, sattr, m, mattr):
    if sattr in s: 
        setattr(m, mattr, s[sattr])

###
# date type conversion

def m2s_date(m, mattr, s, sattr):
    x = getattr(m, mattr)
    if x: s[sattr] = x.isoformat()

def s2m_date(s, sattr, m, mattr):
    if sattr in s: raise Exception, "---- NYI ----" # ---------------------------------  needs work, pyiso8601

###
# dummy no-ops

def m2s_dummy(m, mattr, s, sattr):
    raise Exception, 'something invoked m2s_dummy'

def s2m_dummy(s, sattr, m, mattr):
    raise Exception, 'something invoked s2m_dummy'

###
# request conversion

def r2s_get(r, rname):
    # would use r.REQUEST but I want r.GET to take precedence
    if rname in r.GET: return r.GET[rname]
    elif rname in r.POST: return r.POST[rname]
    else: return None

def r2s_str(r, rname, s):
    x = r2s_get(r, rname)
    if x is not None: s[rname] = x

def r2s_int(r, rname, s):
    x = r2s_get(r, rname)
    if x is not None: s[rname] = int(x)

###
# translation table
# constraints: structure_name (aka: sattr) must be prefixed by the
# name of the class, and therefore the niitial letter must be
# alphabetic; this is necessary for the URL matching to go elegantly.

xtable = (
#(  'structure_name',          'model_attr',       defer_s2m,  r2s_func,  s2m_func,               m2s_func,               ),
(   'commentBody',             'body',             False,      r2s_str,   s2m_string,             m2s_string,             ),
(   'commentCreated',          'created',          False,      r2s_str,   s2m_date,               m2s_date,               ),
(   'commentId',               'id',               False,      r2s_int,   s2m_int,                m2s_int,                ),
(   'commentItem',             'item',             True,       r2s_str,   s2m_commentitem,        m2s_commentitem,        ), # MAKE R2S_INT?
(   'commentLastModified',     'last_modified',    False,      r2s_str,   s2m_date,               m2s_date,               ),
(   'commentLikes',            'likes',            False,      r2s_str,   s2m_int,                m2s_int,                ),
(   'commentRelation',         'relation',         True,       r2s_str,   s2m_commentrelation,    m2s_commentrelation,    ), # ForeignKey
(   'commentTitle',            'title',            False,      r2s_str,   s2m_string,             m2s_string,             ),
(   'itemCreated',             'created',          False,      r2s_str,   s2m_date,               m2s_date,               ),
(   'itemData',                'data',             True,       None,      s2m_dummy,              None,                   ), # FileField
(   'itemDescription',         'description',      False,      r2s_str,   s2m_string,             m2s_string,             ),
(   'itemHideAfter',           'hide_after',       False,      r2s_str,   s2m_date,               m2s_date,               ),
(   'itemHideBefore',          'hide_before',      False,      r2s_str,   s2m_date,               m2s_date,               ),
(   'itemId',                  'id',               False,      r2s_int,   s2m_int,                m2s_int,                ),
(   'itemLastModified',        'last_modified',    False,      r2s_str,   s2m_date,               m2s_date,               ),
(   'itemName',                'name',             False,      r2s_str,   s2m_string,             m2s_string,             ),
(   'itemStatus',              'status',           False,      r2s_str,   s2m_itemstatus,         m2s_itemstatus,         ),
(   'itemTags',                'tags',             True,       r2s_str,   s2m_itemtags,           m2s_itemtags,           ), # ManyToManyField
(   'itemType',                'content_type',     False,      r2s_str,   s2m_string,             m2s_string,             ), # FIX/AUTOFILL
(   'relationCallbackURL',     'url_callback',     False,      r2s_str,   s2m_string,             m2s_string,             ),
(   'relationCreated',         'created',          False,      r2s_str,   s2m_date,               m2s_date,               ),
(   'relationDescription',     'description',      False,      r2s_str,   s2m_string,             m2s_string,             ),
(   'relationEmailAddress',    'email_address',    False,      r2s_str,   s2m_string,             m2s_string,             ),
(   'relationEmbargoAfter',    'embargo_after',    False,      r2s_str,   s2m_date,               m2s_date,               ),
(   'relationEmbargoBefore',   'embargo_before',   False,      r2s_str,   s2m_date,               m2s_date,               ),
(   'relationHomepageURL',     'url_homepage',     False,      r2s_str,   s2m_string,             m2s_string,             ),
(   'relationId',              'id',               False,      r2s_int,   s2m_int,                m2s_int,                ),
(   'relationImageURL',        'url_image',        False,      r2s_str,   s2m_string,             m2s_string,             ),
(   'relationInterests',       'interests',        True,       r2s_str,   s2m_relationinterests,  m2s_relationinterests,  ), # ManyToManyField
(   'relationLastModified',    'last_modified',    False,      r2s_str,   s2m_date,               m2s_date,               ),
(   'relationName',            'name',             False,      r2s_str,   s2m_string,             m2s_string,             ),
(   'relationNetworkPattern',  'network_pattern',  False,      r2s_str,   s2m_string,             m2s_string,             ),
(   'relationVersion',         'version',          False,      r2s_str,   s2m_int,                m2s_int,                ),
(   'tagCreated',              'created',          False,      r2s_str,   s2m_date,               m2s_date,               ),
(   'tagDescription',          'description',      False,      r2s_str,   s2m_string,             m2s_string,             ),
(   'tagId',                   'id',               False,      r2s_int,   s2m_int,                m2s_int,                ),
(   'tagImplies',              'implies',          True,       r2s_str,   s2m_tagimplies,         m2s_tagimplies,         ), # ManyToManyField
(   'tagLastModified',         'last_modified',    False,      r2s_str,   s2m_date,               m2s_date,               ),
(   'tagName',                 'name',             False,      r2s_str,   s2m_string,             m2s_string,             ),
(   'vurlCreated',             'created',          False,      r2s_str,   s2m_date,               m2s_date,               ),
(   'vurlId',                  'id',               False,      r2s_int,   s2m_int,                m2s_int,                ),
(   'vurlLastModified',        'last_modified',    False,      r2s_str,   s2m_date,               m2s_date,               ),
(   'vurlLink',                'link',             False,      r2s_str,   s2m_string,             m2s_string,             ),
(   'vurlName',                'name',             False,      r2s_str,   s2m_string,             m2s_string,             ),
(   'vurlTags',                'tags',             True,       r2s_str,   s2m_vurltags,           m2s_vurltags,           ), # ManyToManyField
    )

###
# table of s-space attribute prefixes and what models they map to

class_prefixes = {
    'comment':   Comment,
    'item':      Item,
    'relation':  Relation,
    'tag':       Tag,
    'vurl':      VanityURL,
    }

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

for (sattr, mattr, defer, r2s_func, s2m_func, m2s_func) in xtable:
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
	raise Exception, "unrecognised prefix in xtable: " + sattr

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
