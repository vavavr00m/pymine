from django.db import models

# Create your models here.

MINE_STRING=1024
EDIT_BACKDOOR=True

class Tag(models.Model):
    name = models.CharField(max_length=MINE_STRING, unique=True)
    description = models.TextField(blank=True)
    implied = models.ManyToManyField('self', symmetrical=False, related_name='x_implied', null=True, blank=True)
    implied_cache = models.ManyToManyField('self', symmetrical=False, related_name='x_implied_cache', null=True, blank=True, editable=EDIT_BACKDOOR)
    date_created = models.DateTimeField(auto_now_add=True, editable=EDIT_BACKDOOR)
    date_last_modified = models.DateTimeField(auto_now=True)
    def __unicode__(self): return self.name


class Relation(models.Model):
    name = models.CharField(max_length=MINE_STRING, unique=True)
    description = models.TextField(blank=True)
    interests = models.ManyToManyField(Tag, related_name='interest_to_relation', null=True, blank=True)
    interests_require = models.ManyToManyField(Tag, related_name='requirement_to_relation', null=True, blank=True)
    interests_exclude = models.ManyToManyField(Tag, related_name='exclusion_to_relation', null=True, blank=True)
    version = models.PositiveIntegerField()
    embargo_after = models.DateTimeField(null=True, blank=True)
    embargo_before = models.DateTimeField(null=True, blank=True)
    ip_address_pattern = models.CharField(max_length=MINE_STRING, blank=True)
    email_address = models.EmailField(max_length=MINE_STRING, blank=True)
    url_callback = models.URLField(max_length=MINE_STRING, blank=True)
    url_homepage = models.URLField(max_length=MINE_STRING, blank=True)
    url_mugshot = models.URLField(max_length=MINE_STRING, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, editable=EDIT_BACKDOOR)
    date_last_modified = models.DateTimeField(auto_now=True)
    def __unicode__(self): return self.name

class Item(models.Model):
    ITEM_STATUSES=(
	( 'PRV', 'Private' ),
	( 'SHD', 'Shared' ),
	( 'PUB', 'Public' ),
	( 'ARQ', 'Authentication Required' ),
	)
    name = models.CharField(max_length=MINE_STRING)
    description = models.TextField(blank=True)
    tags = models.ManyToManyField(Tag, related_name='items_tagged', null=True, blank=True)
    tags_for_relation = models.ManyToManyField(Relation, related_name='items_explicit_for', null=True, blank=True)
    tags_not_relation = models.ManyToManyField(Relation, related_name='items_explicit_not', null=True, blank=True)
    status = models.CharField(max_length=3, choices=ITEM_STATUSES)
    content_type = models.CharField(max_length=MINE_STRING)
    hide_after = models.DateTimeField(null=True, blank=True)
    hide_before = models.DateTimeField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, editable=EDIT_BACKDOOR)
    date_last_modified = models.DateTimeField(auto_now=True)
    def __unicode__(self): return self.name

class Comment(models.Model):
    title = models.CharField(max_length=MINE_STRING)
    body = models.TextField(blank=True)
    likes_this = models.BooleanField(default=False)
    item = models.ForeignKey(Item, editable=EDIT_BACKDOOR)
    relation = models.ForeignKey(Relation, editable=EDIT_BACKDOOR)
    date_created = models.DateTimeField(auto_now_add=True, editable=EDIT_BACKDOOR)
    date_last_modified = models.DateTimeField(auto_now=True)
    def __unicode__(self): return self.title
