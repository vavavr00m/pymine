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

##################################################################

class Tag(models.Model):

    """This is the modelspace representation of the Tag object"""

    name = models.SlugField(max_length=settings.MINE_STRINGSIZE, unique=True)
    description = models.TextField(blank=True)
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
    description = models.TextField(blank=True)
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

    ITEM_STATUSES=(
	( 'X', 'Private' ),
	( 'S', 'Shared' ),
	( 'P', 'Public' ),
	# ( 'A', 'AuthRequired' ),
	)

    ITEM_FS = FileSystemStorage(location=settings.MINE_DBDIR_FILES)

    name = models.CharField(max_length=settings.MINE_STRINGSIZE)
    description = models.TextField(blank=True)
    tags = models.ManyToManyField(Tag, related_name='items_tagged', null=True, blank=True)
    item_for_relations = models.ManyToManyField(Relation, related_name='items_explicitly_for', null=True, blank=True)
    item_not_relations = models.ManyToManyField(Relation, related_name='items_explicitly_not', null=True, blank=True)
    status = models.CharField(max_length=1, choices=ITEM_STATUSES)
    content_type = models.CharField(max_length=settings.MINE_STRINGSIZE)
    data = models.FileField(storage=ITEM_FS, upload_to='%Y/%m/%d')
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

##################################################################

class Comment(models.Model):

    """This is the modelspace representation of the Comment object"""

    title = models.CharField(max_length=settings.MINE_STRINGSIZE)
    body = models.TextField(blank=True)
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
    link = models.TextField(blank=True)
    tags = models.ManyToManyField(Tag, related_name='vurls_tagged', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
	ordering = ['-id']
	verbose_name = 'vanity URL'

    def __unicode__(self):
	return self.name

    def structure(self):
	return model_to_structure('vurl', self)

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
    if mattr != 'item' or sattr != 'commentRelation': raise Exception, "m2s_commentitem is confused"
    pass

def s2m_commentitem(m, mattr, s, sattr):
    if mattr != 'item' or sattr != 'commentRelation': raise Exception, "s2m_commentitem is confused"
    pass

###

def m2s_commentrelation(s, sattr, m, mattr):
    if mattr != 'relation' or sattr != 'commentRelation': raise Exception, "m2s_commentrelation is confused"
    pass

def s2m_commentrelation(s, sattr, m, mattr):
    if mattr != 'relation' or sattr != 'commentRelation': raise Exception, "s2m_commentrelation is confused"
    pass

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

def m2s_itemtags(m, mattr, s, sattr):
    if mattr != 'tags' or sattr != 'itemTags': raise Exception, "m2s_itemtags is confused"

    x = " ".join(x for x in itertools.chain([ i.name for i in m.tags.all() ],
					    [ "for:%s" % i.name for i in m.item_for_relations.all() ],
					    [ "not:%s" % i.name for i in m.item_not_relations.all() ]))
    if x: s[sattr] = x

def s2m_itemtags(s, sattr, m, mattr):
    if mattr != 'tags' or sattr != 'itemTags': raise Exception, "s2m_itemtags is confused"
    pass

###

def m2s_relationinterests(m, mattr, s, sattr):
    if mattr != 'interests' or sattr != 'relationInterests': raise Exception, "m2s_relationinterests is confused"

    x = " ".join(x for x in itertools.chain([ i.name for i in m.tags.all() ],
					    [ "require:%s" % i.name for i in m.tags_required.all() ],
					    [ "exclude:%s" % i.name for i in m.tags_excluded.all() ]))
    if x: s[sattr] = x

def s2m_relationinterests(s, sattr, m, mattr):
    if mattr != 'interests' or sattr != 'relationInterests': raise Exception, "s2m_relationinterests is confused"
    pass

###
# int type conversion

def s2m_int(s, sattr, m, mattr):
    if sattr in s: 
        setattr(m, mattr, s[sattr])

def m2s_int(m, mattr, s, sattr):
    x = getattr(m, mattr)
    if x is not None: s[sattr] = x

###
# string type conversion

def s2m_string(s, sattr, m, mattr):
    if sattr in s: 
        setattr(m, mattr, s[sattr])

def m2s_string(m, mattr, s, sattr):
    x = getattr(m, mattr)
    if x is not None: s[sattr] = x

###
# date type conversion

def s2m_date(s, sattr, m, mattr):
    if sattr in s: raise Exception, "---- NYI ----" # ---------------------------------  needs work, pyiso8601

def m2s_date(m, mattr, s, sattr):
    x = getattr(m, mattr)
    if x: s[sattr] = x.isoformat()

###
# request conversion

def r2s_get(r, rname):
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

xtable = (
#(  'STRUCTURE_NAME',          'MODEL_ATTR',       DEFER_S2M,  R2S_FUNC,  S2M_FUNC,               M2S_FUNC,               ),
(   'commentBody',             'body',             False,      r2s_str,   s2m_string,             m2s_string,             ),
(   'commentCreated',          'created',          False,      r2s_str,   s2m_date,               m2s_date,               ),
(   'commentId',               'id',               False,      r2s_int,   s2m_int,                m2s_int,                ),
(   'commentItem',             'item',             True,       r2s_str,   s2m_commentitem,        m2s_commentitem,        ),
(   'commentLastModified',     'last_modified',    False,      r2s_str,   s2m_date,               m2s_date,               ),
(   'commentLikes',            'likes',            False,      r2s_str,   s2m_int,                m2s_int,                ),
(   'commentRelation',         'relation',         True,       r2s_str,   s2m_commentrelation,    m2s_commentrelation,    ),
(   'commentTitle',            'title',            False,      r2s_str,   s2m_string,             m2s_string,             ),
(   'itemCreated',             'created',          False,      r2s_str,   s2m_date,               m2s_date,               ),
(   'itemDescription',         'description',      False,      r2s_str,   s2m_string,             m2s_string,             ),
(   'itemHideAfter',           'hide_after',       False,      r2s_str,   s2m_date,               m2s_date,               ),
(   'itemHideBefore',          'hide_before',      False,      r2s_str,   s2m_date,               m2s_date,               ),
(   'itemId',                  'id',               False,      r2s_int,   s2m_int,                m2s_int,                ),
(   'itemLastModified',        'last_modified',    False,      r2s_str,   s2m_date,               m2s_date,               ),
(   'itemattr',                'name',             False,      r2s_str,   s2m_string,             m2s_string,             ),
(   'itemStatus',              'status',           False,      r2s_str,   s2m_string,             m2s_string,             ),
(   'itemTags',                'tags',             True,       r2s_str,   s2m_itemtags,           m2s_itemtags,           ),
(   'itemType',                'content_type',     False,      r2s_str,   s2m_string,             m2s_string,             ),  # FIX/AUTOFILL
(   'relationCallbackURL',     'url_callback',     False,      r2s_str,   s2m_string,             m2s_string,             ),
(   'relationCreated',         'created',          False,      r2s_str,   s2m_date,               m2s_date,               ),
(   'relationDescription',     'description',      False,      r2s_str,   s2m_string,             m2s_string,             ),
(   'relationEmailAddress',    'email_address',    False,      r2s_str,   s2m_string,             m2s_string,             ),
(   'relationEmbargoAfter',    'embargo_after',    False,      r2s_str,   s2m_date,               m2s_date,               ),
(   'relationEmbargoBefore',   'embargo_before',   False,      r2s_str,   s2m_date,               m2s_date,               ),
(   'relationHomepageURL',     'url_homepage',     False,      r2s_str,   s2m_string,             m2s_string,             ),
(   'relationId',              'id',               False,      r2s_int,   s2m_int,                m2s_int,                ),
(   'relationImageURL',        'url_image',        False,      r2s_str,   s2m_string,             m2s_string,             ),
(   'relationInterests',       'interests',        True,       r2s_str,   s2m_relationinterests,  m2s_relationinterests,  ),
(   'relationLastModified',    'last_modified',    False,      r2s_str,   s2m_date,               m2s_date,               ),
(   'relationName',            'name',             False,      r2s_str,   s2m_string,             m2s_string,             ),
(   'relationNetworkPattern',  'network_pattern',  False,      r2s_str,   s2m_string,             m2s_string,             ),
(   'relationVersion',         'version',          False,      r2s_str,   s2m_int,                m2s_int,                ),
(   'tagCreated',              'created',          False,      r2s_str,   s2m_date,               m2s_date,               ),
(   'tagDescription',          'description',      False,      r2s_str,   s2m_string,             m2s_string,             ),
(   'tagId',                   'id',               False,      r2s_int,   s2m_int,                m2s_int,                ),
(   'tagImplies',              'implies',          False,      r2s_str,   s2m_tagimplies,         m2s_tagimplies,         ),
(   'tagLastModified',         'last_modified',    False,      r2s_str,   s2m_date,               m2s_date,               ),
(   'tagName',                 'name',             False,      r2s_str,   s2m_string,             m2s_string,             ),
(   'vurlCreated',             'created',          False,      r2s_str,   s2m_date,               m2s_date,               ),
(   'vurlId',                  'id',               False,      r2s_int,   s2m_int,                m2s_int,                ),
(   'vurlLastModified',        'last_modified',    False,      r2s_str,   s2m_date,               m2s_date,               ),
(   'vurlLink',                'link',             False,      r2s_str,   s2m_string,             m2s_string,             ),
(   'vurlName',                'name',             False,      r2s_str,   s2m_string,             m2s_string,             ),
(   'vurlTags',                'tags',             False,      r2s_str,   s2m_vurltags,           m2s_vurltags,           ),
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
defer_table = {}

for prefix in class_prefixes.iterkeys():
    m2s_table[prefix] = {}
    s2m_table[prefix] = {}
    defer_table[prefix] = {} # s2m stuff that requires a DB entry

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
		    defer_table[prefix][sattr] = t
		else:
		    s2m_table[prefix][sattr] = t

	    break
    else:
	raise Exception, "unrecognised prefix in xtable: " + sattr

###
# convert a model to a structure

def model_to_structure(kind, m):
    s = {}
    for mattr, (m2s_func, sattr) in m2s_table[kind].iteritems(): m2s_func(m, mattr, s, sattr)
    return s

###
# convert a request to a model

@transaction.commit_on_success # ie: rollback if it raises an exception
def request_to_save_model(kind, r):
    # create the model
    instantiator = class_prefixes[kind]
    m = instantiator(**m)

    # build a shadow structure: useful for debug/clarity
    s = {}

    # for each target attribute
    for sattr, (r2s_func, s2m_func, mattr) in s2m_table[kind].iteritems():

        # rip the attribute out of the request and convert to python int/str
        s[sattr] = r2s_func(r, sattr, s)

        # s2m the value into the appropriate attribute
        s2m_func(s, sattr, m, mattr)

    # save the model
    m.save()

    # do the deferred (post-save) initialisation
    needs_save = False

    # for each deferred target attribute
    for sattr, (r2s_func, s2m_func, mattr) in defer[kind].iteritems():

        # rip the attribute out of the request and convert to python int/str
        s[sattr] = r2s_func(r, sattr, s)

        # s2m the value into the appropriate attribute
        s2m_func(s, sattr, m, mattr)

        # memento
        needs_save = True

    # update
    if needs_save: m.save()

    # return it
    return m

##################################################################
##################################################################
##################################################################
