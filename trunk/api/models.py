#!/usr/bin/python
##
## Copyright 2010 Adriana Lukas & Alec Muffett
##
## Licensed under the Apache License, Version 2.0 (the "License"); you
## may not use this file except in compliance with the License. You
## may obtain a copy of the License at
##
## http://www.apache.org/licenses/LICENSE-2.0
##
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
## implied. See the License for the specific language governing
## permissions and limitations under the License.
##

"""docstring goes here""" # :-)

#from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
#from django.template.loader import render_to_string
#from django.utils import feedgenerator
from django.conf import settings
from django.core.cache import cache
from django.core.files.storage import FileSystemStorage
from django.db import models, transaction
from django.db.models import Q
from django.utils.encoding import iri_to_uri
from django.utils.http import urlquote

import base64
import string

# TODO:
# phrase tags
# xattrs are represented as $thingAttribute
# envelope for creation can deal with single and multiple returns for create()
# envelope removes status and exit
# multiple file uploads for create
# status flag becomes a bitfield / typed coersce field
# garbage collection for delete

##################################################################
##################################################################
##################################################################

item_fss = FileSystemStorage(location = settings.MINE_DBDIR_FILES)
icon_fss = FileSystemStorage(location = settings.MINE_DBDIR_ICONS)
comment_fss = FileSystemStorage(location = settings.MINE_DBDIR_COMMENTS)
fss_yyyymmdd = '%Y-%m/%d'

##################################################################

item_status_choices = (
    ( '0', 'locked' ),
    ( '2', 'linkable-by-items-in-feeds' ),
    ( '4', 'to-explicitly-cited-feeds' ),
    ( '6', 'to-private-feeds-via-tags' ),
    ( '8', 'to-public-feeds-via-tags' ),
    # In all instances, additional per-item "not:feedname" explicit tagging will be honoured.
    # In all instances, additional per-feed "exclude:tag" explicit tagging will be honoured.
    )

# create a status-lookup table, long->short and short->long
# short->long is ALSO covered by m.get_status_display()

status_lookup = {}
for short, long in item_status_choices:
    status_lookup[long] = short
    status_lookup[short] = long

##################################################################
##################################################################
##################################################################

class Space:
    """library of conversion routines for passing stuff between s-space and m-space"""

    class r2s_lib:
	@staticmethod
	def verbatim(r, s, sattr):
	    """copy a string from a request, to a string in a structure, verbatim"""
	    s[sattr] = str(r.POST[sattr])

	@staticmethod
	def strip(r, s, sattr):
	    """copy a string from a request, to a string in a structure, stripping leading and trailing spaces"""
	    s[sattr] = str(r.POST[sattr]).strip()

	@staticmethod
	def integer(r, s, sattr):
	    """copy a field from a request, to an int in a structure"""
	    s[sattr] = int(r.POST[sattr])

	@staticmethod
	def bool(r, s, sattr):
	    """copy a field from a request, to a bool in a structure"""
	    s[sattr] = True if int(r.POST[sattr]) else False

    class s2m_lib:
	@staticmethod # BACKEND METHOD
	def thingref(klass, s, sattr, m, mattr):
	    """process a foreign key reference"""
	    pass

	@staticmethod
	def itemref(s, sattr, m, mattr):
	    """process a foreign key reference"""
	    return thingref(Item, s, sattr, m, mattr)

	@staticmethod
	def feedref(s, sattr, m, mattr):
	    """process a foreign key reference"""
	    return thingref(Feed, s, sattr, m, mattr)

	@staticmethod # BACKEND METHOD
	def thingreflist(klass, s, sattr, m, mattr):
	    """process a foreign key reference"""
	    pass

	@staticmethod
	def tagreflist(s, sattr, m, mattr):
	    """process a foreign key reference list / manytomany field"""
	    return tagreflist(Tag, s, sattr, m, mattr)

	@staticmethod
	def itemreflist(s, sattr, m, mattr):
	    """process a foreign key reference list / manytomany field"""
	    return tagreflist(Item, s, sattr, m, mattr)

	@staticmethod
	def feedreflist(s, sattr, m, mattr):
	    """process a foreign key reference list / manytomany field"""
	    return tagreflist(Feed, s, sattr, m, mattr)

	@staticmethod
	def dummy(s, sattr, m, mattr):
	    """do nothing"""
	    pass

	@staticmethod
	def copy(s, sattr, m, mattr):
	    """copy a field in a structure, to a field in a model, preserving type"""
	    if sattr in s: setattr(m, mattr, s[sattr])

	@staticmethod
	def strip(s, sattr, m, mattr):
	    """copy a field (assume type string) in a structure, to a string in a model, stripping leading and trailing spaces"""
	    if sattr in s: setattr(m, mattr, s[sattr].strip())

	@staticmethod
	def date(s, sattr, m, mattr):
	    """copy a date in a structure, to a date in a model"""
	    if sattr in s:
		raise RuntimeError, "not yet integrated the Date parser"

	@staticmethod
	def bool(s, sattr, m, mattr):
	    """copy a bool in a structure, to a bool in a model"""
	    if sattr in s:
		if s[sattr]:
		    setattr(m, mattr, True)
		else:
		    setattr(m, mattr, False)

    class m2s_lib:
	@staticmethod # BACKEND METHOD
	def thingref(klass, m, mattr, s, sattr):
	    """process a foreign key reference"""
	    pass

	@staticmethod
	def itemref(m, mattr, s, sattr):
	    """process a foreign key reference"""
	    return thingref(Item, m, mattr, s, sattr)

	@staticmethod
	def feedref(m, mattr, s, sattr):
	    """process a foreign key reference"""
	    return thingref(Feed, m, mattr, s, sattr)

	@staticmethod # BACKEND METHOD
	def thingreflist(klass, m, mattr, s, sattr):
	    """process a foreign key reference"""
	    pass

	@staticmethod
	def tagreflist(m, mattr, s, sattr):
	    """process a foreign key reference list / manytomany field"""
	    return tagreflist(Tag, m, mattr, s, sattr)

	@staticmethod
	def itemreflist(m, mattr, s, sattr):
	    """process a foreign key reference list / manytomany field"""
	    return tagreflist(Item, m, mattr, s, sattr)

	@staticmethod
	def feedreflist(m, mattr, s, sattr):
	    """process a foreign key reference list / manytomany field"""
	    return tagreflist(Feed, m, mattr, s, sattr)

	@staticmethod
	def dummy(m, mattr, s, sattr):
	    """do nothing"""
	    pass

	@staticmethod
	def copy(m, mattr, s, sattr):
	    """copy a field in a model, to a field in a structure, preserving type"""
	    x = getattr(m, mattr)
	    if x: s[sattr] = x

	@staticmethod
	def date(m, mattr, s, sattr):
	    """copy a date in a model, to a date in a structure"""
	    x = getattr(m, mattr)
	    if x: s[sattr] = x.isoformat()

	@staticmethod
	def bool(m, mattr, s, sattr):
	    """copy a field in a model, to a field in a structure"""
	    x = getattr(m, mattr)
	    if x:
		s[sattr] = 1
	    else:
		s[sattr] = 0

    class gc_lib:
	@staticmethod
	def to_null(m, mattr):
	    """trash a field in a model, by nulling it (not secure delete). requires save()"""
	    setattr(m, matter, None)

	@staticmethod
	def dereference(m, mattr):
	    """trash a field in a model, by unreferencing it (not secure delete). requires save()"""
	    pass

	@staticmethod
	def dereflist(m, mattr):
	    """trash a field in a model, by unreferencing the contents (not secure delete). requires save()"""
	    pass

	@staticmethod
	def defile(m, mattr):
	    """trash a file in a model by deleting it (not likely to be secure delete).  requires save()"""
	    pass

	@staticmethod
	def to_blank(m, mattr):
	    """trash a field in a model by blanking it (not secure delete). requires save()"""
	    setattr(m, matter, "")

	@staticmethod
	def to_zero(m, mattr):
	    """trash a field in a model by setting it to 0 (not secure delete). requires save()"""
	    setattr(m, matter, 0)

	@staticmethod
	def to_false(m, mattr):
	    """trash a field in a model by setting it to False (not secure delete). requires save()"""
	    setattr(m, matter, False)

	@staticmethod
	def to_unique(m, mattr):
	    """trash a field in a model by filling it with hopefully unique garbage (not secure delete). requires save()"""
	    setattr(m, mattr, "__%s_%d_%s__" % (mattr, m.id, 'RANDOM_GARBAGE_TBD'))

    @staticmethod
    def compile(attr_map):
	"""
	return the three compiled conversion tables for moving/updating a thing between
	r- to s- space
	s- to m- space
	m- to s- space
	"""

	r2s = {}
	s2m = {}
	m2s = {}
	gc = {}

	def barf(direction, mattr, sattr):
	    """to be called when methud exists but is empty"""
	    raise RuntimeError, 'blank methud for %s, %s, %s' % (direction, mattr, sattr)

	prefix = attr_map.pop('__prefix__')

	for mattr in attr_map.keys():
	    table = attr_map[mattr]
	    sattr = prefix + "".join([ string.capitalize(x) for x in mattr.split("_") ])

	    # print mattr, "->", sattr

	    if 'm2s' in table:
		methud = getattr(Space.m2s_lib, table['m2s'])
		if not methud: barf('m2s', mattr, sattr)
		m2s[mattr] = lambda m, s: methud(m, mattr, s, sattr)

	    if 's2m' in table:
		methud = getattr(Space.s2m_lib, table['s2m'])
		if not methud: barf('s2m', mattr, sattr)
		s2m[sattr] = lambda s, m: methud(s, sattr, m, mattr)
		r2s[sattr] = lambda r, s: Space.r2s_lib.strip(r, s, sattr) # default to r2s.strip()

	    if 'r2s' in table: # override default provided in s2m
		methud = getattr(Space.r2s_lib, table['r2s'])
		if not methud: barf('r2s', mattr, sattr)
		r2s[sattr] = lambda r, s: methud(r, s, sattr)

	    if mattr == 'id':
		pass # id fields do not get gc'ed
	    elif 'gc' in table:
		methud = getattr(Space.gc_lib, table['gc'])
		gc[mattr] = lambda m: methud(m, mattr)
	    else:
		gc[mattr] = lambda m: gc_lib.to_null(m, mattr) # default to_null()

	return (r2s, s2m, m2s, gc)

##################################################################
##################################################################
##################################################################

class AbstractField:
    """superclass to frontend model fields and ease porting between GAE and Django"""

    STRING_SHORT = 256 # bytes

    class Meta:
	abstract = True

    @staticmethod
    def parse(input):
	"""
	Argument parser/translater for AbstractField.

	One dict comes in, another goes out.

	implements unique, symmetrical, storage, upload_to, pivot
	"""

	if input.get('required', True):
	    output = dict(null=False, blank=False)
	else:
	    output = dict(null=True, blank=True)

	for iname, oname in (('unique', 'unique'),
			     ('symmetrical', 'symmetrical'),
			     ('storage', 'storage'),
			     ('upload_to', 'upload_to'),
			     ('pivot', 'related_name'),
			     ):
	    if iname in input:
		output[oname] = input[iname]

	return output

    @staticmethod
    def bool(default):
	"""implements a bool (true/false)"""
	return models.BooleanField(default=default)

    @staticmethod
    def choice(choices):
	"""implements a choices-field (max length of an encoded choice is 1 character)"""
	return models.CharField(max_length=1, choices=choices)

    @staticmethod
    def created():
	"""implements created date"""
	return models.DateTimeField(auto_now_add=True)

    @staticmethod
    def datetime(**kwargs):
	"""implements date/time field"""
	x = AbstractField.parse(kwargs)
	return models.DateTimeField(**x)

    @staticmethod
    def file(**kwargs):
	"""implements a file"""
	x = AbstractField.parse(kwargs)
	return models.FileField(**x)

    @staticmethod
    def integer(default):
	"""implements an integer"""
	return models.PositiveIntegerField(default=default)

    @staticmethod
    def last_modified():
	"""implements last_modified date"""
	return models.DateTimeField(auto_now=True)

    @staticmethod
    def reference(what, **kwargs):
	"""implements foreign-keys"""
	x = AbstractField.parse(kwargs)
	return models.ForeignKey(what, **x)

    @staticmethod
    def reflist(what, **kwargs):
	"""implements list-of-foreign-keys; AbstractField.parses out 'pivot' argument"""
	x = AbstractField.parse(kwargs)
	return models.ManyToManyField(what, **x)

    @staticmethod
    def slug(**kwargs):
	"""implements a slug (alphanumeric string, no spaces)"""
	x = AbstractField.parse(kwargs)
	return models.SlugField(max_length=AbstractField.STRING_SHORT, **x)

    @staticmethod
    def string(**kwargs):
	"""implements string"""
	x = AbstractField.parse(kwargs)
	return models.CharField(max_length=AbstractField.STRING_SHORT, **x)

    @staticmethod
    def text(**kwargs):
	"""implements a text area / text of arbitrary size"""
	x = AbstractField.parse(kwargs)
	return models.TextField(**x)

    @staticmethod
    def url(**kwargs):
	"""implements a URL string"""
	x = AbstractField.parse(kwargs)
	return models.URLField(max_length=AbstractField.STRING_SHORT, **x)

##################################################################
##################################################################
##################################################################

class AbstractModel(models.Model):
    """superclass to frontend models and ease porting between GAE and Django"""

    class Meta:
	abstract = True

    created = AbstractField.created()
    last_modified = AbstractField.last_modified()

    @classmethod
    def get(klass, **kwargs):
	"""return a single model matching kwargs; expunge virtually-deleted ones; if none return None; if multiple, throw exception"""
	pass

    @classmethod
    def list(klass, **kwargs):
	"""return a queryset of models matching kwargs; expunge virtually-deleted ones"""
	pass

    @classmethod
    def search(klass, search_string, **kwargs):
	"""return a queryset of models matching search_string; expunge virtually-deleted ones"""
	pass

    @classmethod
    def all(klass, **kwargs):
	"""return a queryset of models matching kwargs; INCLUDE virtually-deleted ones"""
	pass

##################################################################
##################################################################
##################################################################

class AbstractXattr(AbstractModel):
    """superclass to frontend extended attributes"""

    class Meta:
	abstract = True

    key = AbstractField.slug()
    value = AbstractField.text()

    def __unicode__(self):
	"""return the name of this xattr"""
	return self.key

##################################################################

class TagXattr(AbstractXattr):
    """tag extended attributes"""

    class Meta:
	ordering = ['key']
	unique_together = ('tag', 'key')
	verbose_name = 'TagXattr'

    tag = AbstractField.reference('Tag')

##################################################################

class VurlXattr(AbstractXattr):
    """vurl extended attributes"""

    class Meta:
	ordering = ['key']
	unique_together = ('vurl', 'key')
	verbose_name = 'VurlXattr'

    vurl = AbstractField.reference('Vurl')

##################################################################

class FeedXattr(AbstractXattr):
    """feed extended attributes"""

    class Meta:
	ordering = ['key']
	unique_together = ('feed', 'key')
	verbose_name = 'FeedXattr'

    feed = AbstractField.reference('Feed')

##################################################################

class ItemXattr(AbstractXattr):
    """item extended attributes"""

    class Meta:
	ordering = ['key']
	unique_together = ('item', 'key')
	verbose_name = 'ItemXattr'

    item = AbstractField.reference('Item')

##################################################################

class CommentXattr(AbstractXattr):
    """comment extended attributes"""

    class Meta:
	ordering = ['key']
	unique_together = ('comment', 'key')
	verbose_name = 'CommentXattr'

    comment = AbstractField.reference('Comment')

##################################################################
##################################################################
##################################################################

class AbstractThing(AbstractModel):
    """superclass for all the major mine types"""

    class Meta:
	abstract = True

    attr_map = {
	'__prefix__': "thing",
	}

    (r2s, s2m, m2s, gc) = Space.compile(attr_map)

    id = 0
    name = 'thing'
    is_deleted = AbstractField.bool(False)

    @classmethod
    def create(self, request=None, **kwargs):
	"""
	create a new Thing from a HTTPRequest, overriding with values from kwargs.

	NB: for Item() ONLY: create one or more new Items() from a
	HTTPRequest, overriding with values from kwargs; assuming
	nothing goes wrong, one Item() will be created per "data" file
	submitted in the multipart POST request.  If no "data" file is
	submitted, only a single non-data Item will result.  The
	result for a single Item() creation will be a single Item().
	The result for multiple Item() creation will be a list of
	multiple Items().  For Item() creation via the API, all this
	will be made plain via the envelope metadata.
	"""
	pass

    def update(self, request=None, **kwargs):
	"""update a single Thing from a HTTPRequest, overriding with values from kwargs"""
	pass

    def delete(self):
	"""gc all the fields and mark this Thing as deleted"""

	for mattr in self.gc.keys():
	    self.gc[mattr](self)

	self.is_deleted = True
	self.save()

    def to_structure(self):
	"""convert this model m to a dictionary structure s (ie: s-space)"""
	pass

    def get_absolute_url(self):
	"""return a url for this object for administrative purposes"""
	url = u''
	return iri_to_uri(url)

    def set_attribute(self, key, value):
	"""set attribute 'key' (or extended attribute for '$key') to 'value' (a string)"""
	pass

    def get_attribute(self, key):
	"""get the value of attribute 'key' (or extended attribute for '$key')"""
	pass

    def delete_attribute(self, key):
	"""erase the value of attribute 'key' (or delete extended attribute '$key')"""
	pass

    def list_attributes(self):
	"""list all attributes and $extendedattributes"""
	pass

    def __unicode__(self):
	"""return the canonical name of this object"""
	return self.name

##################################################################

class Tag(AbstractThing):
    attr_map = {
	'__prefix__': "tag",
	'id': dict(r2s='integer', s2m='copy', m2s='copy'),
	'created': dict(s2m='date', m2s='date'),
	'last_modified': dict(s2m='date', m2s='date'),

	'name': dict(s2m='copy', m2s='copy'),
	'description': dict(r2s='verbatim', s2m='copy', m2s='copy'),
	'implies': dict(s2m='dummy', m2s='dummy'),
	'cloud': dict(s2m='dummy', m2s='dummy'),
	}
    (r2s, s2m, m2s, gc) = Space.compile(attr_map)

    name = AbstractField.slug(unique=True)
    description = AbstractField.text(required=False)
    implies = AbstractField.reflist('self', symmetrical=False, pivot='implied_by', required=False)
    cloud = AbstractField.reflist('self', symmetrical=False, pivot='clouded_by', required=False)

##################################################################

class Vurl(AbstractThing):
    attr_map = {
	'__prefix__': "vurl",
	'id': dict(r2s='integer', s2m='copy', m2s='copy'),
	'created': dict(s2m='date', m2s='date'),
	'last_modified': dict(s2m='date', m2s='date'),

	'name': dict(s2m='copy', m2s='copy'),
	'link': dict(s2m='copy', m2s='copy'),
	'invalid_before': dict(s2m='date', m2s='date'),
	'invalid_after': dict(s2m='date', m2s='date'),
	'use_temporary_redirect': dict(r2s='bool', s2m='bool', m2s='bool'),
	}
    (r2s, s2m, m2s, gc) = Space.compile(attr_map)

    name = AbstractField.slug(unique=True)
    link = AbstractField.text(unique=True)
    invalid_before = AbstractField.datetime(required=False)
    invalid_after = AbstractField.datetime(required=False)
    use_temporary_redirect = AbstractField.bool(False)

##################################################################

class Feed(AbstractThing):
    attr_map = {
	'__prefix__': "feed",
	'id': dict(r2s='integer', s2m='copy', m2s='copy'),
	'created': dict(s2m='date', m2s='date'),
	'last_modified': dict(s2m='date', m2s='date'),

	'name': dict(s2m='copy', m2s='copy'),
	'version': dict(s2m='dummy', m2s='dummy'),
	'description': dict(r2s='verbatim', s2m='copy', m2s='copy'),
	'embargo_after': dict(s2m='date', m2s='date'),
	'embargo_before': dict(s2m='date', m2s='date'),
	'tags': dict(s2m='dummy', m2s='dummy'),
	'tags_exclude': dict(s2m='dummy', m2s='dummy'),
	'tags_require': dict(s2m='dummy', m2s='dummy'),
	'permitted_networks': dict(s2m='copy', m2s='copy'),
	'content_constraints': dict(s2m='copy', m2s='copy'),
	'is_private': dict(r2s='bool', s2m='bool', m2s='bool'),
	}
    (r2s, s2m, m2s, gc) = Space.compile(attr_map)

    name = AbstractField.slug(unique=True)
    version = AbstractField.integer(1)
    description = AbstractField.text(required=False)
    embargo_after = AbstractField.datetime(required=False)
    embargo_before = AbstractField.datetime(required=False)
    tags = AbstractField.reflist(Tag, pivot='feeds_with_tag', required=False)
    tags_exclude = AbstractField.reflist(Tag, pivot='feeds_excluding', required=False)
    tags_require = AbstractField.reflist(Tag, pivot='feeds_requiring', required=False)
    permitted_networks = AbstractField.string(required=False)
    content_constraints = AbstractField.string(required=False)
    is_private = AbstractField.bool(True)

##################################################################

class Item(AbstractThing):
    attr_map = {
	'__prefix__': "item",
	'id': dict(r2s='integer', s2m='copy', m2s='copy'),
	'created': dict(s2m='date', m2s='date'),
	'last_modified': dict(s2m='date', m2s='date'),

	'name': dict(s2m='copy', m2s='copy'),
	'status': dict(s2m='dummy', m2s='dummy'),
	'description': dict(r2s='verbatim', s2m='copy', m2s='copy'),
	'hide_after': dict(s2m='date', m2s='date'),
	'hide_before': dict(s2m='date', m2s='date'),
	'tags': dict(s2m='dummy', m2s='dummy'),
	'item_for_feeds': dict(s2m='dummy', m2s='dummy'),
	'item_not_feeds': dict(s2m='dummy', m2s='dummy'),
	'data': dict(s2m='dummy', m2s='dummy'),
	'data_type': dict(s2m='copy', m2s='copy'),
	'data_remote_url': dict(s2m='copy', m2s='copy'),
	'linked_items': dict(s2m='dummy', m2s='dummy'),
	'encryption_method': dict(s2m='copy', m2s='copy'),
	'digest_method': dict(s2m='copy', m2s='copy'),
	'encryption_key': dict(s2m='copy', m2s='copy'),
	'ciphertext_digest': dict(s2m='copy', m2s='copy'),
	'icon': dict(s2m='dummy', m2s='dummy'),
	'icon_type': dict(s2m='copy', m2s='copy'),
	'icon_ciphertext_digest': dict(s2m='copy', m2s='copy'),
	}
    (r2s, s2m, m2s, gc) = Space.compile(attr_map)

    name = AbstractField.string()
    status = AbstractField.choice(item_status_choices)
    description = AbstractField.text(required=False)
    hide_after = AbstractField.datetime(required=False)
    hide_before = AbstractField.datetime(required=False)
    tags = AbstractField.reflist(Tag, pivot='items_tagged', required=False)
    item_for_feeds = AbstractField.reflist(Feed, pivot='items_explicitly_for', required=False)
    item_not_feeds = AbstractField.reflist(Feed, pivot='items_explicitly_not', required=False)

    data = AbstractField.file(storage=item_fss, upload_to=fss_yyyymmdd, required=False)
    data_type = AbstractField.string(required=False)
    data_remote_url = AbstractField.url(required=False)

    linked_items = AbstractField.reflist('Item', pivot='items_linked', required=False)

    encryption_method = AbstractField.text(required=False)
    digest_method = AbstractField.text(required=False)
    encryption_key = AbstractField.text(required=False)
    ciphertext_digest = AbstractField.text(required=False)

    icon = AbstractField.file(storage=icon_fss, upload_to=fss_yyyymmdd, required=False)
    icon_type = AbstractField.string(required=False)
    icon_ciphertext_digest = AbstractField.text(required=False)

##################################################################

class Comment(AbstractThing):
    attr_map = {
	'__prefix__': "comment",
	'id': dict(r2s='integer', s2m='copy', m2s='copy'),
	'created': dict(s2m='date', m2s='date'),
	'last_modified': dict(s2m='date', m2s='date'),

	'title': dict(s2m='copy', m2s='copy'),
	'body': dict(r2s='verbatim', s2m='copy', m2s='copy'),
	'from_feed': dict(s2m='dummy', m2s='dummy'),
	'upon_item': dict(s2m='dummy', m2s='dummy'),
	'data': dict(s2m='dummy', m2s='dummy'),
	'encryption_method': dict(s2m='copy', m2s='copy'),
	'digest_method': dict(s2m='copy', m2s='copy'),
	'encryption_key': dict(s2m='copy', m2s='copy'),
	'ciphertext_digest': dict(s2m='copy', m2s='copy'),
	}

    (r2s, s2m, m2s, gc) = Space.compile(attr_map)

    title = AbstractField.string()
    body = AbstractField.text(required=False)
    from_feed = AbstractField.reference(Feed, required=False)
    upon_item = AbstractField.reference(Item, required=False)

    data = AbstractField.file(storage=comment_fss, upload_to=fss_yyyymmdd, required=False)

    encryption_method = AbstractField.text(required=False)
    digest_method = AbstractField.text(required=False)
    encryption_key = AbstractField.text(required=False)
    ciphertext_digest = AbstractField.text(required=False)

    def __unicode__(self):
	"""return the title of this comment; comments lack a "name" field"""
	return self.title

##################################################################

class Registry(AbstractModel): # not a Thing
    """key/value pairs for Mine configuration"""

    key = AbstractField.slug(unique=True)
    value = AbstractField.text()

    @classmethod
    def get(klass, key):
	""" """
	return Registry.objects.get(key=key).value

    @classmethod
    def get_decoded(klass, key):
	""" """
	return base64.urlsafe_b64decode(klass.get(key))

    @classmethod
    def set(klass, key, value, overwrite_ok):
	""" """
	r, created = Registry.objects.get_or_create(key=key, defaults={ 'value': value })
	if not created and not int(overwrite_ok):
	    raise RuntimeError, 'not allowed to overwrite existing Registry key: %s' % key
	r.save()
	return r

    @classmethod
    def set_encoded(klass, key, value, overwrite_ok):
	""" """
	return klass.set(key, base64.urlsafe_b64encode(value), overwrite_ok)

    def to_structure(self):
	""" """
	s = {}
	s[self.key] = self.value # this is why it is not a Thing
	s['keyCreated'] = self.created.isoformat()
	s['keyLastModified'] = self.last_modified.isoformat()
	return s

    class Meta:
	ordering = ['key']
	verbose_name = 'Register'
	verbose_name_plural = 'Registry'

    def __unicode__(self):
	return self.key

##################################################################

class Event(AbstractModel): # not a Thing
    """audit trail for Mine"""

    message = AbstractField.string()
    alert = AbstractField.bool(False)

    feed = AbstractField.reference(Feed, required=False)
    item = AbstractField.reference(Item, required=False)
    ip_address = AbstractField.string(required=False)
    method = AbstractField.string(required=False)
    url = AbstractField.string(required=False)
