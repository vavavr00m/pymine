from django.db import models

# Create your models here.

MINE_STRING=1024

class Item(models.Model):
    ITEM_STATUSES=(
        ( 'PRV', 'Private' ),
        ( 'SHD', 'Shared' ),
        ( 'PUB', 'Public' ),
        ( 'ARQ', 'Authentication Required' ),
        )

    name = models.CharField(max_length=MINE_STRING)
    description = models.TextField(blank=True)
    tags = models.CharField(max_length=MINE_STRING, blank=True)
    status = models.CharField(max_length=3, choices=ITEM_STATUSES)

    content_type = models.CharField(max_length=MINE_STRING)
    hide_after = models.DateTimeField(blank=True)
    hide_before = models.DateTimeField(blank=True)

    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_last_modified = models.DateTimeField(auto_now=True)

class Relation(models.Model):
    name = models.CharField(max_length=MINE_STRING, unique=True)
    description = models.TextField(blank=True)
    interests = models.CharField(max_length=MINE_STRING, blank=True)
    version = models.PositiveIntegerField()

    embargo_after = models.DateTimeField(blank=True)
    embargo_before = models.DateTimeField(blank=True)
    ip_address_pattern = models.CharField(max_length=MINE_STRING, blank=True)

    email_address = models.EmailField(max_length=MINE_STRING, blank=True)
    url_callback = models.URLField(max_length=MINE_STRING, blank=True)
    url_homepage = models.URLField(max_length=MINE_STRING, blank=True)
    url_mugshot = models.URLField(max_length=MINE_STRING, blank=True)

    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_last_modified = models.DateTimeField(auto_now=True)

class Tag(models.Model):
    name = models.CharField(max_length=MINE_STRING, unique=True)
    implied = models.CharField(max_length=MINE_STRING, blank=True)

    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_last_modified = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    title = models.CharField(max_length=MINE_STRING)
    body = models.TextField(blank=True)
    likes_this = models.BooleanField(default=False)

    item = models.ForeignKey(Item, editable=False)
    relation = models.ForeignKey(Relation, editable=False)

    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_last_modified = models.DateTimeField(auto_now=True)
