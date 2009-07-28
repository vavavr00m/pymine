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
EDIT_BACKDOOR=True

##################################################################

class Tag(models.Model):
    name = models.SlugField(max_length=MINE_STRING, unique=True)
    description = models.TextField(blank=True)
    implies = models.ManyToManyField('self', symmetrical=False, related_name='x_implies', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=EDIT_BACKDOOR)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta: ordering = ['id']

    def structure(self):
	s = {}
	s['tagId'] = int(self.id)
	x = self.name
        if x: s['tagName'] = x
	x = self.description
	if x: s['tagDescription'] = x
	x = ' '.join([ x.name for x in self.implies.all() ])
	if x: s['tagImplies'] = x
	x = self.created
	if x: s['tagCreated'] = x.isoformat()
	x = self.last_modified
	if x: s['tagLastModified'] = x.isoformat()
	return s

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

    class Meta: ordering = ['name']

    def structure(self):
	s = {}
	s['relationId'] = int(self.id)
	x = self.name
        if x: s['relationName'] = x
	x = self.description
        if x: s['relationDescription'] = x
	x = self.version
        if x: s['relationVersion'] = x
	x = self.embargo_before
        if x: s['relationEmbargoBefore'] = x.isoformat()
	x = self.embargo_after
        if x: s['relationEmbargoAfter'] = x.isoformat()
	x = self.network_pattern
        if x: s['relationNetworkPattern'] = x
	x = self.email_address
        if x: s['relationEmailAddress'] = x
	x = self.url_callback
        if x: s['relationCallbackURL'] = x
	x = self.url_homepage
        if x: s['relationHomepageURL'] = x
	x = self.url_image
        if x: s['relationImageURL'] = x
	x = self.created
        if x: s['relationCreated'] = x.isoformat()
	x = self.last_modified
        if x: s['relationLastModified'] = x.isoformat()
	x = " ".join(x for x in itertools.chain( [ i.name for i in self.tags.all() ], 
                                                 [ "require:%s" % i.name for i in self.tags_required.all() ], 
                                                 [ "exclude:%s" % i.name for i in self.tags_excluded.all() ]))
        if x: s['relationInterests'] = x
	return s

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

    class Meta: ordering = ['-last_modified']

    def structure(self):
	s = {}
	s['itemId'] = int(self.id)
        x = self.name
        if x: s['itemName'] = x
        x = self.description
        if x: s['itemDescription'] = x
        x = self.status
        if x: s['itemStatus'] = x
        x = self.content_type
        if x: s['itemType'] = x
        x = self.hide_after.isoformat()
        if x: s['itemHideAfter'] = x
        x = self.hide_before.isoformat()
        if x: s['itemHideBefore'] = x
        x = self.created.isoformat()
        if x: s['itemCreated'] = x
        x = self.last_modified.isoformat()
        if x: s['itemLastModified'] = x
	x = " ".join(x for x in itertools.chain( [ i.name for i in self.tags.all() ], 
                                                 [ "for:%s" % i.name for i in self.item_for_relations.all() ], 
                                                 [ "not:%s" % i.name for i in self.item_not_relations.all() ]))
        if x: s['itemTags'] = x
        return s


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

    class Meta: ordering = ['-id']

    def structure(self):
	s = {}
	s['commentId'] = int(self.id)
        x = self.title
        if x: s['commentTitle'] = x
        x = self.body
        if x: s['commentBody'] = x
        x = self.likes
        if x: s['commentLikes'] = x
        x = self.item
        if x: s['commentItem'] = x.id
        x = self.relation
        if x: s['commentRelation'] = x.name
        x = self.created
        if x: s['commentCreated'] = x.isoformat()
        x = self.last_modified
        if x: s['commentLastModified'] = x.isoformat()
        return s

    def __unicode__(self):
	return self.title

##################################################################

class VanityURL(models.Model):
    name = models.SlugField(max_length=MINE_STRING, unique=True)
    link = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=EDIT_BACKDOOR)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta: ordering = ['-id']

    def __unicode__(self):
	return self.name

##################################################################
