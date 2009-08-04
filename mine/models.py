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

from django.db import models, transaction

import itertools

MINE_STRING=1024
EDIT_BACKDOOR=False

##################################################################

class Tag(models.Model):

    #"""This is the modelspace representation of the Tag object"""

    name = models.SlugField(max_length=MINE_STRING, unique=True)
    description = models.TextField(blank=True)
    implies = models.ManyToManyField('self', symmetrical=False, related_name='x_implies', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=EDIT_BACKDOOR)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
	ordering = ['name']

    def __unicode__(self):
	return self.name

    def structure(self):
	return model_to_structure('tag', self)

##################################################################

class Relation(models.Model):

    #"""This is the modelspace representation of the Relation object"""

    name = models.SlugField(max_length=MINE_STRING, unique=True)
    description = models.TextField(blank=True)
    tags = models.ManyToManyField(Tag, related_name='relations_with_tag', null=True, blank=True)
    tags_required = models.ManyToManyField(Tag, related_name='relations_requiring', null=True, blank=True)
    tags_excluded = models.ManyToManyField(Tag, related_name='relations_excluding', null=True, blank=True)
    version = models.PositiveIntegerField(default=1)
    embargo_after = models.DateTimeField(null=True, blank=True)
    embargo_before = models.DateTimeField(null=True, blank=True)
    network_pattern = models.CharField(max_length=MINE_STRING, blank=True)
    email_address = models.EmailField(max_length=MINE_STRING, blank=True)
    url_callback = models.URLField(max_length=MINE_STRING, blank=True)
    url_homepage = models.URLField(max_length=MINE_STRING, blank=True)
    url_image = models.URLField(max_length=MINE_STRING, blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=EDIT_BACKDOOR)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
	ordering = ['name']

    def __unicode__(self):
	return self.name

    def structure(self):
	return model_to_structure('relation', self)

##################################################################

class Item(models.Model):

    #"""This is the modelspace representation of the Item object"""

    ITEM_STATUSES=(
	( 'X', 'Private' ),
	( 'S', 'Shared' ),
	( 'P', 'Public' ),
	( 'A', 'AuthRequired' ),
	)

    name = models.CharField(max_length=MINE_STRING)
    description = models.TextField(blank=True)
    tags = models.ManyToManyField(Tag, related_name='items_tagged', null=True, blank=True)
    item_for_relations = models.ManyToManyField(Relation, related_name='items_explicitly_for', null=True, blank=True)
    item_not_relations = models.ManyToManyField(Relation, related_name='items_explicitly_not', null=True, blank=True)
    status = models.CharField(max_length=1, choices=ITEM_STATUSES)
    content_type = models.CharField(max_length=MINE_STRING)
    hide_after = models.DateTimeField(null=True, blank=True)
    hide_before = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=EDIT_BACKDOOR)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
	ordering = ['-last_modified']

    def __unicode__(self):
	return self.name

    def structure(self):
	return model_to_structure('item', self)

##################################################################

class Comment(models.Model):

    #"""This is the modelspace representation of the Comment object"""

    title = models.CharField(max_length=MINE_STRING)
    body = models.TextField(blank=True)
    likes = models.BooleanField(default=False)
    item = models.ForeignKey(Item)
    relation = models.ForeignKey(Relation)
    created = models.DateTimeField(auto_now_add=True, editable=EDIT_BACKDOOR)
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

    name = models.SlugField(max_length=MINE_STRING, unique=True)
    link = models.TextField(blank=True)
    tags = models.ManyToManyField(Tag, related_name='vurls_tagged', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=EDIT_BACKDOOR)
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

def m2s_tagimplies(m, mname, s, sname):
    if mname != 'implies': raise Exception, "m2s_tagimplies is confused"
    x = ' '.join([ x.name for x in m.implies.all() ])
    if x: s[sname] = x

def s2m_tagimplies(s, sname, m, mname): ################################################################## <- issue is here, must save before setting relations
    if sname != 'tagImplies': raise Exception, "s2m_tagimplies is confused"
    if sname in s:
	for x in s[sname].split():
	    t = Tag.objects.get(name=x)
	    m.implies.add(t)

def m2s_vurltags(m, mname, s, sname):
    if mname != '': raise Exception, "m2s_vurltags is confused"
    x = ' '.join([ x.name for x in m.tags.all() ])
    if x: s[sname] = x

###

def m2s_itemtags(m, mname, s, sname):
    if mname != '': raise Exception, "m2s_itemtags is confused"
    x = " ".join(x for x in itertools.chain([ i.name for i in m.tags.all() ],
					    [ "for:%s" % i.name for i in m.item_for_relations.all() ],
					    [ "not:%s" % i.name for i in m.item_not_relations.all() ]))
    if x: s[sname] = x

###

def m2s_relationinterests(m, mname, s, sname):
    if mname != '': raise Exception, "m2s_relationinterests is confused"
    x = " ".join(x for x in itertools.chain([ i.name for i in m.tags.all() ],
					    [ "require:%s" % i.name for i in m.tags_required.all() ],
					    [ "exclude:%s" % i.name for i in m.tags_excluded.all() ]))
    if x: s[sname] = x

###
# int type conversion

def s2m_int(s, sname, m, mname):
    if sname in s: m[mname] = s[sname]

def m2s_int(m, mname, s, sname):
    x = getattr(m, mname)
    if x: s[sname] = x

###
# string type conversion

def s2m_string(s, sname, m, mname):
    if sname in s: m[mname] = s[sname]

def m2s_string(m, mname, s, sname):
    x = getattr(m, mname)
    if x: s[sname] = x

###
# date type conversion

def s2m_date(s, sname, m, mname):
    if sname in s: raise Exception, "---- NYI ----" # ---------------------------------  needs work

def m2s_date(m, mname, s, sname):
    x = getattr(m, mname)
    if x: s[sname] = x.isoformat()

###
# request conversion # --------------------------------- MAY NEED TO BE HACKED LATER, SOMETIMES EMPTY VALUE IS LEGIT FOR UPDATE, ETC

def req_get_str(r, rname):
    if rname in r.GET: return r.GET[rname]
    elif rname in r.POST: return r.POST[rname]
    else: return None

def req_get_int(r, rname):
    x = req_get_str(r, rname)
    if x: return int(x)
    else: return None

###
# translation table

xtable = (
#(  'structureName',           'model_attr',       defer_s2m,  req_get_func,  s2m_func,        m2s_func,               ),
(   'commentBody',             'body',             False,          req_get_str,   s2m_string,      m2s_string,             ),
(   'commentCreated',          'created',          False,          req_get_str,   s2m_date,        m2s_date,               ),
(   'commentId',               'id',               False,          req_get_int,   s2m_int,         m2s_int,                ),
(   'commentItem',             'item',             True,           req_get_str,   None,                None,                       ),
(   'commentLastModified',     'last_modified',    False,          req_get_str,   s2m_date,        m2s_date,               ),
(   'commentLikes',            'likes',            False,          req_get_str,   s2m_int,         m2s_int,                ),
(   'commentRelation',         'relation',         True,           req_get_str,   None,                None,                       ),
(   'commentTitle',            'title',            False,          req_get_str,   s2m_string,      m2s_string,             ),
(   'itemCreated',             'created',          False,          req_get_str,   s2m_date,        m2s_date,               ),
(   'itemDescription',         'description',      False,          req_get_str,   s2m_string,      m2s_string,             ),
(   'itemHideAfter',           'hide_after',       False,          req_get_str,   s2m_date,        m2s_date,               ),
(   'itemHideBefore',          'hide_before',      False,          req_get_str,   s2m_date,        m2s_date,               ),
(   'itemId',                  'id',               False,          req_get_int,   s2m_int,         m2s_int,                ),
(   'itemLastModified',        'last_modified',    False,          req_get_str,   s2m_date,        m2s_date,               ),
(   'itemName',                'name',             False,          req_get_str,   s2m_string,      m2s_string,             ),
(   'itemStatus',              'status',           False,          req_get_str,   s2m_string,      m2s_string,             ),
(   'itemTags',                'tags',             True,           req_get_str,   None,                m2s_itemtags,           ),
(   'itemType',                'content_type',     False,          req_get_str,   s2m_string,      m2s_string,             ),
(   'relationCallbackURL',     'url_callback',     False,          req_get_str,   s2m_string,      m2s_string,             ),
(   'relationCreated',         'created',          False,          req_get_str,   s2m_date,        m2s_date,               ),
(   'relationDescription',     'description',      False,          req_get_str,   s2m_string,      m2s_string,             ),
(   'relationEmailAddress',    'email_address',    False,          req_get_str,   s2m_string,      m2s_string,             ),
(   'relationEmbargoAfter',    'embargo_after',    False,          req_get_str,   s2m_date,        m2s_date,               ),
(   'relationEmbargoBefore',   'embargo_before',   False,          req_get_str,   s2m_date,        m2s_date,               ),
(   'relationHomepageURL',     'url_homepage',     False,          req_get_str,   s2m_string,      m2s_string,             ),
(   'relationId',              'id',               False,          req_get_int,   s2m_int,         m2s_int,                ),
(   'relationImageURL',        'url_image',        False,          req_get_str,   s2m_string,      m2s_string,             ),
(   'relationInterests',       'interests',        True,           req_get_str,   None,                m2s_relationinterests,  ),
(   'relationLastModified',    'last_modified',    False,          req_get_str,   s2m_date,        m2s_date,               ),
(   'relationName',            'name',             False,          req_get_str,   s2m_string,      m2s_string,             ),
(   'relationNetworkPattern',  'network_pattern',  False,          req_get_str,   s2m_string,      m2s_string,             ),
(   'relationVersion',         'version',          False,          req_get_str,   s2m_int,         m2s_int,                ),
(   'tagCreated',              'created',          False,          req_get_str,   s2m_date,        m2s_date,               ),
(   'tagDescription',          'description',      False,          req_get_str,   s2m_string,      m2s_string,             ),
(   'tagId',                   'id',               False,          req_get_int,   s2m_int,         m2s_int,                ),
(   'tagImplies',              'implies',          False,          req_get_str,   s2m_tagimplies,  m2s_tagimplies,         ),
(   'tagLastModified',         'last_modified',    False,          req_get_str,   s2m_date,        m2s_date,               ),
(   'tagName',                 'name',             False,          req_get_str,   s2m_string,      m2s_string,             ),
(   'vurlCreated',             'created',          False,          req_get_str,   s2m_date,        m2s_date,               ),
(   'vurlId',                  'id',               False,          req_get_int,   s2m_int,         m2s_int,                ),
(   'vurlLastModified',        'last_modified',    False,          req_get_str,   s2m_date,        m2s_date,               ),
(   'vurlLink',                'link',             False,          req_get_str,   s2m_string,      m2s_string,             ),
(   'vurlName',                'name',             False,          req_get_str,   s2m_string,      m2s_string,             ),
(   'vurlTags',                'tags',             False,          req_get_str,   None,                m2s_vurltags,           ),
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

for (sname, mname, defer, req_get_func, s2m_func, m2s_func) in xtable:
    for prefix in class_prefixes.iterkeys():

	if sname.startswith(prefix):
	    if m2s_func:
		m2s_table[prefix][mname] = (m2s_func, sname)

	    if s2m_func:
		t = (s2m_func, mname, req_get_func)

		if defer:
		    defer_table[prefix][sname] = t
		else:
		    s2m_table[prefix][sname] = t

	    break
    else:
	raise Exception, "unrecognised prefix in xtable: " + sname

###
# convert a model to a structure

def model_to_structure(kind, m):
    s = {}
    for mname, (m2s_func, sname) in m2s_table[kind].iteritems(): m2s_func(m, mname, s, sname)
    return s

###
# convert a request to a model

@transaction.commit_on_success # ie: rollback if it raises an exception
def request_to_saved_model(kind, r):
    # create a blank kwargs
    ma = {}

.....................................
    for sname, (mfunc, mname, req_get_func) in s2m_table[kind].iteritems():
	v = req_get_func(r, sname) # retreive the value from the request
	s2m_func(s, sname, ma, mname)

    # work out what kind of model we are creating, and initialise one with the kwargs
    instantiator = class_prefixes[kind]
    m = instantiator(**ma)

    # save it
    m.save()

    # do deferred relationship initialisation
    poked = False

    for sname, (mfunc, mname, req_get_func) in defer_table[kind].iteritems():
	poked = True
.................................


    if poked: m.save()

    # return it
    return m

##################################################################
##################################################################
##################################################################
