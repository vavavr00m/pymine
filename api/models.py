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
	def bool(r, s, sattr):
	    """copy a field from a request, to a bool in a structure"""
	    s[sattr] = True if int(r.POST[sattr]) else False

	@staticmethod
	def integer(r, s, sattr):
	    """copy a field from a request, to an int in a structure"""
	    s[sattr] = int(r.POST[sattr])

	@staticmethod # THIS IS THE DEFAULT HARDCODED R2S_LIB METHOD
	def strip(r, s, sattr):
	    """copy a string from a request, to a string in a structure, stripping leading and trailing spaces"""
	    s[sattr] = str(r.POST[sattr]).strip()

	@staticmethod
	def verbatim(r, s, sattr):
	    """copy a string from a request, to a string in a structure, verbatim"""
	    s[sattr] = str(r.POST[sattr])

    class s2m_lib:
	@staticmethod
	def comment_from_feed(s, sattr, m, mattr):
	    """ """
	    pass

	@staticmethod
	def comment_upon_item(s, sattr, m, mattr):
	    """ """
	    pass

	@staticmethod
	def feed_tags(s, sattr, m, mattr):
	    """ """
	    pass

	@staticmethod
	def feed_tags_exclude(s, sattr, m, mattr):
	    """ """
	    pass

	@staticmethod
	def feed_tags_require(s, sattr, m, mattr):
	    """ """
	    pass

	@staticmethod
	def item_for_feeds(s, sattr, m, mattr):
	    """ """
	    pass

	@staticmethod
	def item_links_to_items(s, sattr, m, mattr):
	    """ """
	    pass

	@staticmethod
	def item_not_feeds(s, sattr, m, mattr):
	    """ """
	    pass

	@staticmethod
	def item_tags(s, sattr, m, mattr):
	    """ """
	    pass

	@staticmethod
	def item_status(s, sattr, m, mattr):
	    """ """
	    pass

	@staticmethod
	def tag_implies(s, sattr, m, mattr):
	    """ """
	    pass

	@staticmethod
	def bool(s, sattr, m, mattr):
	    """copy a bool in a structure, to a bool in a model"""
	    if sattr in s:
		if s[sattr]:
		    setattr(m, mattr, True)
		else:
		    setattr(m, mattr, False)
	@staticmethod
	def copy(s, sattr, m, mattr):
	    """copy a field in a structure, to a field in a model, preserving type"""
	    if sattr in s: setattr(m, mattr, s[sattr])

	@staticmethod
	def date(s, sattr, m, mattr):
	    """copy a date in a structure, to a date in a model"""
	    if sattr in s:
		raise RuntimeError, "not yet integrated the Date parser"

	@staticmethod
	def strip(s, sattr, m, mattr):
	    """copy a field (assume type string) in a structure, to a string in a model, stripping leading and trailing spaces"""
	    if sattr in s: setattr(m, mattr, s[sattr].strip())


    class m2s_lib:
	@staticmethod
	def comment_from_feed(m, mattr, s, sattr):
	    """ """
	    pass

	@staticmethod
	def comment_upon_item(m, mattr, s, sattr):
	    """ """
	    pass

	@staticmethod
	def feed_tags(m, mattr, s, sattr):
	    """ """
	    pass

	@staticmethod
	def feed_tags_exclude(m, mattr, s, sattr):
	    """ """
	    pass

	@staticmethod
	def feed_tags_require(m, mattr, s, sattr):
	    """ """
	    pass

	@staticmethod
	def item_for_feeds(m, mattr, s, sattr):
	    """ """
	    pass

	@staticmethod
	def item_links_to_items(m, mattr, s, sattr):
	    """ """
	    pass

	@staticmethod
	def item_not_feeds(m, mattr, s, sattr):
	    """ """
	    pass

	@staticmethod
	def item_tags(m, mattr, s, sattr):
	    """ """
	    pass

	@staticmethod
	def item_status(m, mattr, s, sattr):
	    """ """
	    pass

	@staticmethod
	def tag_cloud(m, mattr, s, sattr):
	    """ """
	    pass

	@staticmethod
	def tag_implies(m, mattr, s, sattr):
	    """ """
	    pass

	@staticmethod
	def bool(m, mattr, s, sattr):
	    """copy a field in a model, to a field in a structure"""
	    x = getattr(m, mattr)
	    if x:
		s[sattr] = 1
	    else:
		s[sattr] = 0
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

    class gc_lib:
	@staticmethod
	def skip(m, mattr):
	    """do not trash a field"""
	    pass

	@staticmethod
	def nullify(m, mattr):
	    """trash a field in a model, by nulling it (not secure delete). requires save()"""
	    setattr(m, matter, None)

	@staticmethod
	def reflist(m, mattr):
	    """trash a field in a model, by unreferencing the contents (not secure delete). requires save()"""
	    pass

	@staticmethod
	def file(m, mattr):
	    """trash a file in a model by deleting it (not likely to be secure delete).  requires save()"""
	    pass

	@staticmethod
	def blankify(m, mattr):
	    """trash a field in a model by blanking it (not secure delete). requires save()"""
	    setattr(m, matter, "")

	@staticmethod
	def zeroify(m, mattr):
	    """trash a field in a model by setting it to 0 (not secure delete). requires save()"""
	    setattr(m, matter, 0)

	@staticmethod
	def falsify(m, mattr):
	    """trash a field in a model by setting it to False (not secure delete). requires save()"""
	    setattr(m, matter, False)

	@staticmethod
	def munge(m, mattr):
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

        defer_table = {
            'commentFromFeed': True,
            'commentUponItem': True,
            'feedTags': True,
            'feedTagsExclude': True,
            'feedTagsRequire': True,
            'itemData': True,
            'itemForFeeds': True,
            'itemIcon': True,
            'itemLinksToItems': True,
            'itemNotFeeds': True,
            'itemTags': True,
            'tagCloud': True,
            'tagImplies': True,
            }

	def barf(direction, mattr, sattr):
	    """to be called when methud exists but is empty"""
	    raise RuntimeError, 'blank methud for %s, %s, %s' % (direction, mattr, sattr)

	prefix = attr_map.pop('__prefix__')

	for mattr in attr_map.keys():
	    table = attr_map[mattr]
	    sattr = prefix + "".join([ string.capitalize(x) for x in mattr.split("_") ])

	    # print prefix + "." + mattr, "->", sattr

	    if 'm2s' in table:
		methud = getattr(Space.m2s_lib, table['m2s'])
		if not methud: barf('m2s', mattr, sattr)
		m2s[mattr] = lambda m, s: methud(m, mattr, s, sattr)

	    if 's2m' in table:
		methud = getattr(Space.s2m_lib, table['s2m'])
		if not methud: barf('s2m', mattr, sattr)
		s2m[sattr] = ( defer_table.get(sattr, False), lambda s, m: methud(s, sattr, m, mattr) )
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
		gc[mattr] = lambda m: gc_lib.nullify(m, mattr) # default nullify()

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
    def create(klass, request=None, **kwargs):
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
        margs = {}
        m = klass(**margs)
        return m.update(request, **kwargs)

    @classmethod
    def get(klass, **kwargs):
	"""return a single model matching kwargs; expunge virtually-deleted ones; if none return None; if multiple, throw exception"""
	return klass.objects.filter(is_deleted=False).get(**kwargs)

    @classmethod
    def list(klass, **kwargs):
	"""return a queryset of models matching kwargs; expunge virtually-deleted ones"""
	return klass.objects.filter(is_deleted=False).filter(**kwargs)

    @classmethod
    def execute_search_query(klass, search_string, qs):
        """take one queryset and return another, filtered by the content of search_string; this version is a no-op"""
        return qs

    @classmethod
    def search(klass, search_string, **kwargs):
	"""return a queryset of models matching **kwargs and search_string; expunge virtually-deleted ones"""
	return klass.execute_search_query(search_string, klass.list(**kwargs))

    def update(self, request=None, **kwargs):
	"""update a single Thing from a HTTPRequest, overriding with values from kwargs"""

        # build a shadow structure: useful for debug/clarity                                                                         
        s = {}

        # update shadow structure from request and kwargs
        for sattr in self.r2s.keys():
            if sattr in kwargs: 
                s[sattr] = kwargs[sattr]
            elif request and sattr in r.POST: 
                self.r2s[sattr](request, s)    
            else: 
                continue # kinda redundant but clearer

        # update self from shadow structure

        # stage 1: undeferred
        i_changed_something = False

        for sattr in self.s2m.keys():
            methud, defer = self.s2m[sattr]
            if not defer:
                methud(s, self)
                i_changed_something = True

        # the point of deferral is to save a record so there is an Id,
        # so that foreign keys can work and files can be saved; so
        # it's only really relevant if there is no Id

        if i_changed_something and not self.id:
            self.save() # generate an id

        # stage 2: deferred
        i_changed_something = False

        for sattr in self.s2m.keys():
            methud, defer = self.s2m[sattr]
            if defer:
                methud(s, self)
                i_changed_something = True

        if i_changed_something:
            self.save()

        # stage 3: file saving
        # do this by subclassing

    def delete(self): # this is the primary consumer of gc
	"""gc all the fields and mark this Thing as deleted"""
	for mattr in self.gc.keys(): 
            self.gc[mattr](self)
	self.is_deleted = True
	self.save()

    def to_structure(self): # this is the primary consumer of m2s
	"""convert this model m to a dictionary structure s (ie: s-space)"""
	s = {}
        for mattr in self.m2s.keys(): 
            self.m2s[mattr](self, s)
        return s
        
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
	'created': dict(gc='skip', s2m='date', m2s='date'),
	'last_modified': dict(gc='skip', s2m='date', m2s='date'),

	'name': dict(gc='munge', s2m='copy', m2s='copy'),
	'description': dict(r2s='verbatim', s2m='copy', m2s='copy'),
	'implies': dict(gc='reflist', s2m='tag_implies', m2s='tag_implies'),
	'cloud': dict(gc='reflist', m2s='tag_cloud'),
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
	'created': dict(gc='skip', s2m='date', m2s='date'),
	'last_modified': dict(gc='skip', s2m='date', m2s='date'),

	'name': dict(gc='munge', s2m='copy', m2s='copy'),
	'link': dict(gc='munge', s2m='copy', m2s='copy'),
	'invalid_before': dict(s2m='date', m2s='date'),
	'invalid_after': dict(s2m='date', m2s='date'),
	'use_temporary_redirect': dict(gc='falsify', r2s='bool', s2m='bool', m2s='bool'),
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
	'created': dict(gc='skip', s2m='date', m2s='date'),
	'last_modified': dict(gc='skip', s2m='date', m2s='date'),

	'name': dict(gc='munge', s2m='copy', m2s='copy'),
	'version': dict(gc='zeroify', r2s='integer', s2m='copy', m2s='copy'),
	'description': dict(r2s='verbatim', s2m='copy', m2s='copy'),
	'embargo_after': dict(s2m='date', m2s='date'),
	'embargo_before': dict(s2m='date', m2s='date'),
	'tags': dict(gc='reflist', s2m='feed_tags', m2s='feed_tags'),
	'tags_exclude': dict(gc='reflist', s2m='feed_tags_exclude', m2s='feed_tags_exclude'),
	'tags_require': dict(gc='reflist', s2m='feed_tags_require', m2s='feed_tags_require'),
	'permitted_networks': dict(s2m='copy', m2s='copy'),
	'content_constraints': dict(s2m='copy', m2s='copy'),
	'is_private': dict(gc='falsify', r2s='bool', s2m='bool', m2s='bool'),
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
	'created': dict(gc='skip', s2m='date', m2s='date'),
	'last_modified': dict(gc='skip', s2m='date', m2s='date'),

	'name': dict(gc='munge', s2m='copy', m2s='copy'),
	'status': dict(gc='skip', s2m='item_status', m2s='item_status'),
	'description': dict(r2s='verbatim', s2m='copy', m2s='copy'),
	'hide_after': dict(s2m='date', m2s='date'),
	'hide_before': dict(s2m='date', m2s='date'),
	'tags': dict(gc='reflist', s2m='item_tags', m2s='item_tags'),
	'for_feeds': dict(gc='reflist', s2m='item_for_feeds', m2s='item_for_feeds'),
	'not_feeds': dict(gc='reflist', s2m='item_not_feeds', m2s='item_not_feeds'),
	'data_type': dict(s2m='copy', m2s='copy'),
	'data_remote_url': dict(s2m='copy', m2s='copy'),
	'links_to_items': dict(gc='reflist', s2m='item_links_to_items', m2s='item_links_to_items'),
	'encryption_method': dict(s2m='copy', m2s='copy'),
	'digest_method': dict(s2m='copy', m2s='copy'),
	'encryption_key': dict(s2m='copy', m2s='copy'),
	'ciphertext_digest': dict(s2m='copy', m2s='copy'),
	'icon_type': dict(s2m='copy', m2s='copy'),
	'icon_ciphertext_digest': dict(s2m='copy', m2s='copy'),

        'data': dict(gc='file'),
        'icon': dict(gc='file'),
	}
    (r2s, s2m, m2s, gc) = Space.compile(attr_map)

    name = AbstractField.string()
    status = AbstractField.choice(item_status_choices)
    description = AbstractField.text(required=False)
    hide_after = AbstractField.datetime(required=False)
    hide_before = AbstractField.datetime(required=False)
    tags = AbstractField.reflist(Tag, pivot='items_tagged', required=False)
    for_feeds = AbstractField.reflist(Feed, pivot='items_explicitly_for', required=False)
    not_feeds = AbstractField.reflist(Feed, pivot='items_explicitly_not', required=False)

    data = AbstractField.file(storage=item_fss, upload_to=fss_yyyymmdd, required=False) # not translated
    data_type = AbstractField.string(required=False)
    data_remote_url = AbstractField.url(required=False)

    links_to_items = AbstractField.reflist('Item', pivot='item_linked_from', required=False)

    encryption_method = AbstractField.text(required=False)
    digest_method = AbstractField.text(required=False)
    encryption_key = AbstractField.text(required=False)
    ciphertext_digest = AbstractField.text(required=False)

    icon = AbstractField.file(storage=icon_fss, upload_to=fss_yyyymmdd, required=False) # not translated
    icon_type = AbstractField.string(required=False)
    icon_ciphertext_digest = AbstractField.text(required=False)

##################################################################

class Comment(AbstractThing):
    attr_map = {
	'__prefix__': "comment",
	'id': dict(r2s='integer', s2m='copy', m2s='copy'),
	'created': dict(gc='skip', s2m='date', m2s='date'),
	'last_modified': dict(gc='skip', s2m='date', m2s='date'),

	'title': dict(gc='munge', s2m='copy', m2s='copy'),
	'body': dict(r2s='verbatim', s2m='copy', m2s='copy'),
	'from_feed': dict(s2m='comment_from_feed', m2s='comment_from_feed'),
	'upon_item': dict(s2m='comment_upon_item', m2s='comment_upon_item'),
	'encryption_method': dict(s2m='copy', m2s='copy'),
	'digest_method': dict(s2m='copy', m2s='copy'),
	'encryption_key': dict(s2m='copy', m2s='copy'),
	'ciphertext_digest': dict(s2m='copy', m2s='copy'),

        'data': dict(gc='file'),
	}

    (r2s, s2m, m2s, gc) = Space.compile(attr_map)

    title = AbstractField.string()
    body = AbstractField.text(required=False)
    from_feed = AbstractField.reference(Feed, required=False)
    upon_item = AbstractField.reference(Item, required=False)

    data = AbstractField.file(storage=comment_fss, upload_to=fss_yyyymmdd, required=False) # not translated

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
