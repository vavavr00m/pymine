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
    name = models.SlugField(max_length=MINE_STRING, unique=True)
    description = models.TextField(blank=True)
    implies = models.ManyToManyField('self', symmetrical=False, related_name='x_implies', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=EDIT_BACKDOOR)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']

    def __unicode__(self):
	return self.name

##################################################################

class Relation(models.Model):
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

##################################################################

class Item(models.Model):
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

##################################################################

class Comment(models.Model):
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

##################################################################

class VanityURL(models.Model):
    name = models.SlugField(max_length=MINE_STRING, unique=True)
    link = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=EDIT_BACKDOOR)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']

    def __unicode__(self):
	return self.name

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
    def s2m_date():
        pass

    def m2s_date():
        pass

    def s2m_int():
        pass

    def m2s_int():
        pass

    def s2m_string():
        pass

    def m2s_string():
        pass

    def s2m_NYI():
        pass

    def m2s_NYI():
        pass

    # ( structureName, 'model_attribute', s2m_func, m2s_func ),
    xtable = (
        ('commentBody',             'body',             s2m_string,  m2s_string  ),
        ('commentCreated',          'created',          None,        m2s_date    ),
        ('commentId',               'id',               None,        m2s_int     ),
        ('commentItem',             'item',             s2m_NYI,     m2s_NYI     ),
        ('commentLastModified',     'last_modified',    None,        m2s_date    ),
        ('commentLikes',            'likes',            s2m_int,     m2s_int     ),
        ('commentRelation',         'relation',         s2m_NYI,     m2s_NYI     ),
        ('commentTitle',            'title',            s2m_string,  m2s_string  ),
        ('itemCreated',             'created',          None,        m2s_date    ),
        ('itemDescription',         'description',      s2m_string,  m2s_string  ),
        ('itemHideAfter',           'hide_after',       s2m_date,    m2s_date    ),
        ('itemHideBefore',          'hide_before',      s2m_date,    m2s_date    ),
        ('itemId',                  'id',               None,        m2s_int     ),
        ('itemLastModified',        'last_modified',    None,        m2s_date    ),
        ('itemName',                'name',             s2m_string,  m2s_string  ),
        ('itemStatus',              'status',           s2m_string,  m2s_string  ),
        ('itemTags',                'tags',             s2m_NYI,     m2s_NYI     ),
        ('itemType',                'content_type',     s2m_string,  m2s_string  ),
        ('relationCallbackURL',     'url_callback',     s2m_string,  m2s_string  ),
        ('relationCreated',         'created',          None,        m2s_date    ),
        ('relationDescription',     'description',      s2m_string,  m2s_string  ),
        ('relationEmailAddress',    'email_address',    s2m_string,  m2s_string  ),
        ('relationEmbargoAfter',    'embargo_after',    s2m_date,    m2s_date    ),
        ('relationEmbargoBefore',   'embargo_before',   s2m_date,    m2s_date    ),
        ('relationHomepageURL',     'url_homepage',     s2m_string,  m2s_string  ),
        ('relationId',              'id',               None,        m2s_int     ),
        ('relationImageURL',        'url_image',        s2m_string,  m2s_string  ),
        ('relationInterests',       'interests',        s2m_NYI,     m2s_NYI     ),
        ('relationLastModified',    'last_modified',    None,        m2s_date    ),
        ('relationName',            'name',             s2m_string,  m2s_string  ),
        ('relationNetworkPattern',  'network_pattern',  s2m_string,  m2s_string  ),
        ('relationVersion',         'version',          s2m_int,     m2s_int     ),
        ('tagCreated',              'created',          None,        m2s_date    ),
        ('tagDescription',          'description',      s2m_string,  m2s_string  ),
        ('tagId',                   'id',               None,        m2s_int     ),
        ('tagImplies',              'implies',          s2m_NYI,     m2s_NYI     ),
        ('tagLastModified',         'last_modified',    None,        m2s_date    ),
        ('tagName',                 'name',             s2m_string,  m2s_string  ),
        )

    def model_to_structure():
        pass

    def structure_to_model(id=0):
        pass

    def request_to_structure():
        pass

    def request_to_model(id=0):
        pass

