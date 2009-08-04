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

from django.db import models
import itertools

MINE_STRING=1024
EDIT_BACKDOOR=False

##################################################################

class Tag(models.Model):

    """This is the modelspace representation of the Tag object"""

    name = models.SlugField(max_length=MINE_STRING, unique=True)
    description = models.TextField(blank=True)
    implies = models.ManyToManyField('self', symmetrical=False, related_name='x_implies', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=EDIT_BACKDOOR)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']

    def __unicode__(self):
	return self.name

    def structure():
        return Transcoder.model_to_structure('tag', self)

##################################################################

class Relation(models.Model):

    """This is the modelspace representation of the Relation object"""

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

    def structure():
        return Transcoder.model_to_structure('relation', self)

##################################################################

class Item(models.Model):

    """This is the modelspace representation of the Item object"""

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

    def structure():
        return Transcoder.model_to_structure('item', self)

##################################################################

class Comment(models.Model):

    """This is the modelspace representation of the Comment object"""

    title = models.CharField(max_length=MINE_STRING)
    body = models.TextField(blank=True)
    likes = models.BooleanField(default=False)
    item = models.ForeignKey(Item, editable=EDIT_BACKDOOR)
    relation = models.ForeignKey(Relation, editable=EDIT_BACKDOOR)
    created = models.DateTimeField(auto_now_add=True, editable=EDIT_BACKDOOR)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']

    def __unicode__(self):
	return self.title

    def structure():
        return Transcoder.model_to_structure('comment', self)

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

    def __unicode__(self):
	return self.name

    def structure():
        return Transcoder.model_to_structure('vurl', self)

##################################################################
##################################################################
##################################################################

# x = ' '.join([ x.name for x in self.implies.all() ])

# x = " ".join(x for x in itertools.chain( [ i.name for i in self.tags.all() ], 
# [ "require:%s" % i.name for i in self.tags_required.all() ], 
# [ "exclude:%s" % i.name for i in self.tags_excluded.all() ]))

# x = " ".join(x for x in itertools.chain( [ i.name for i in self.tags.all() ], 
# [ "for:%s" % i.name for i in self.item_for_relations.all() ], 
# [ "not:%s" % i.name for i in self.item_not_relations.all() ]))


class Transcoder():

    """Transcoder provides a lot of the security for pymine; it converts
    between 'client-space' structural s-representations of data as
    (approximately) specified in the protomine API, and the
    Django-internal model-based m-representations; the reason for
    doing this is partly philosophic - that there should be a clearly
    defined breakpoint between the two worlds, and this is it; if we
    just serialized models and slung them back and forth, the mine
    would be wedded to Django evermore, which is not a good thing."""

    def s2m_date(s, sname, m, mname):
        raise Exception, "nyi"

    def m2s_date(m, mname, s, sname):
        if mname in m:
            s[sname] = m[mname].isoformat()

    def s2m_int(s, sname, m, mname):
        if sname in s:
            m[mname] = s[sname]
        
    def m2s_int(m, mname, s, sname):
        if mname in m:
            s[sname] = m[mname]

    def s2m_string(s, sname, m, mname):
        if sname in s:
            m[mname] = s[sname]

    def m2s_string(m, mname, s, sname):
        if mname in m:
            s[sname] = m[mname]

    def s2m_NYI(s, sname, m, mname):
        raise Exception, "nyi"

    def m2s_NYI(m, mname, s, sname):
        raise Exception, "nyi"

    # ( structureName, 'model_attribute', s2m_func, m2s_func ),
    xtable = (
        ('commentBody',             'body',             s2m_string,  m2s_string  ),
        ('commentCreated',          'created',          s2m_date,    m2s_date    ),
        ('commentId',               'id',               None,        m2s_int     ),
        ('commentItem',             'item',             s2m_NYI,     m2s_NYI     ),
        ('commentLastModified',     'last_modified',    s2m_date,    m2s_date    ),
        ('commentLikes',            'likes',            s2m_int,     m2s_int     ),
        ('commentRelation',         'relation',         s2m_NYI,     m2s_NYI     ),
        ('commentTitle',            'title',            s2m_string,  m2s_string  ),
        ('itemCreated',             'created',          s2m_date,    m2s_date    ),
        ('itemDescription',         'description',      s2m_string,  m2s_string  ),
        ('itemHideAfter',           'hide_after',       s2m_date,    m2s_date    ),
        ('itemHideBefore',          'hide_before',      s2m_date,    m2s_date    ),
        ('itemId',                  'id',               None,        m2s_int     ),
        ('itemLastModified',        'last_modified',    s2m_date,    m2s_date    ),
        ('itemName',                'name',             s2m_string,  m2s_string  ),
        ('itemStatus',              'status',           s2m_string,  m2s_string  ),
        ('itemTags',                'tags',             s2m_NYI,     m2s_NYI     ),
        ('itemType',                'content_type',     s2m_string,  m2s_string  ),
        ('relationCallbackURL',     'url_callback',     s2m_string,  m2s_string  ),
        ('relationCreated',         'created',          s2m_date,    m2s_date    ),
        ('relationDescription',     'description',      s2m_string,  m2s_string  ),
        ('relationEmailAddress',    'email_address',    s2m_string,  m2s_string  ),
        ('relationEmbargoAfter',    'embargo_after',    s2m_date,    m2s_date    ),
        ('relationEmbargoBefore',   'embargo_before',   s2m_date,    m2s_date    ),
        ('relationHomepageURL',     'url_homepage',     s2m_string,  m2s_string  ),
        ('relationId',              'id',               None,        m2s_int     ),
        ('relationImageURL',        'url_image',        s2m_string,  m2s_string  ),
        ('relationInterests',       'interests',        s2m_NYI,     m2s_NYI     ),
        ('relationLastModified',    'last_modified',    s2m_date,    m2s_date    ),
        ('relationName',            'name',             s2m_string,  m2s_string  ),
        ('relationNetworkPattern',  'network_pattern',  s2m_string,  m2s_string  ),
        ('relationVersion',         'version',          s2m_int,     m2s_int     ),
        ('tagCreated',              'created',          s2m_date,    m2s_date    ),
        ('tagDescription',          'description',      s2m_string,  m2s_string  ),
        ('tagId',                   'id',               None,        m2s_int     ),
        ('tagImplies',              'implies',          s2m_NYI,     m2s_NYI     ),
        ('tagLastModified',         'last_modified',    s2m_date,    m2s_date    ),
        ('tagName',                 'name',             s2m_string,  m2s_string  ),
        ('vurmCreated',             'created',          s2m_date,    m2s_date    ),
        ('vurmId',                  'id',               None,        m2s_int     ),
        ('vurmLastModified',        'last_modified',    s2m_date,    m2s_date    ),
        ('vurmLink',                'link',             s2m_string,  m2s_string  ),
        ('vurmName',                'name',             s2m_string,  m2s_string  ),
        ('vurmTags',                'tags',             s2m_NYI,     m2s_NYI     ),
        )

    m2s_table = {}
    m2s_table['comment'] = {}
    m2s_table['item'] = {}
    m2s_table['relation'] = {}
    m2s_table['tag'] = {}

    s2m_table = {}
    s2m_table['comment'] = {}
    s2m_table['item'] = {}
    s2m_table['relation'] = {}
    s2m_table['tag'] = {}

    for (sname, mname, s2mfunc, m2sfunc) in xtable:
        if sname.startswith('comment'):
            if m2sfunc: m2s_table['comment'][mname] = (m2sfunc, sname)
            if s2mfunc: s2m_table['comment'][sname] = (s2mfunc, mname)

        elif sname.startswith('item'):
            if m2sfunc: m2s_table['item'][mname] = (m2sfunc, sname)
            if s2mfunc: s2m_table['item'][sname] = (s2mfunc, mname)

        elif sname.startswith('relation'):
            if m2sfunc: m2s_table['relation'][mname] = (m2sfunc, sname)
            if s2mfunc: s2m_table['relation'][sname] = (s2mfunc, mname)

        elif sname.startswith('tag'):
            if m2sfunc: m2s_table['tag'][mname] = (m2sfunc, sname)
            if s2mfunc: s2m_table['tag'][sname] = (s2mfunc, mname)

        else:
            raise Exception, "unrecognised prefix in xtable"

    def model_to_structure(kind, m):
        s = {}

        for mname, (m2sfunc, sname) in m2s_table[kind]:
            m2sfunc(m, mname, s, sname)

        return s

    def structure_to_model(kind, s, id=0):
        m = {}

        for sname, (s2mfunc, mname) in s2m_table[kind]:
            s2mfunc(s, sname, m, mname)

        if kind == 'item':
            return Item(**m)
        if kind == 'tag':
            return Tag(**m)
        if kind == 'relation':
            return Relation(**m)
        if kind == 'comment':
            return Comment(**m)
        else:
            raise Exception, "unrecognised 'kind' in structure_to_model()"

    def request_to_structure(kind, r):
        raise Exception, "nyi"

    def request_to_model(kind, r, id=0):
        s = request_to_structure(kind, r)
        return(structure_to_model(kind, s, id)
