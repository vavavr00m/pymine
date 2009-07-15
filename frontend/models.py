from django.db import models

# Create your models here.

MINE_STRING=1024
EDIT_BACKDOOR=True

class Tag(models.Model):
    name = models.CharField(max_length=MINE_STRING, unique=True)
    description = models.TextField(blank=True)
    implies = models.ManyToManyField('self', symmetrical=False, related_name='x_implies', null=True, blank=True)
    cached_implications = models.ManyToManyField('self', symmetrical=False, related_name='x_cached_implications', null=True, blank=True, editable=EDIT_BACKDOOR)
    date_created = models.DateTimeField(auto_now_add=True, editable=EDIT_BACKDOOR)
    date_last_modified = models.DateTimeField(auto_now=True)
    def __unicode__(self): return self.name


class Relation(models.Model):
    name = models.CharField(max_length=MINE_STRING, unique=True)
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
    item_for_relations = models.ManyToManyField(Relation, related_name='items_explicitly_for', null=True, blank=True)
    item_not_relations = models.ManyToManyField(Relation, related_name='items_explicitly_not', null=True, blank=True)
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
