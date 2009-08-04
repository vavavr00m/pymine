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
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
## implied. See the License for the specific language governing
## permissions and limitations under the License.
##

#from pymine.mine.models import Item, Relation, Tag, Comment

# Transcoder provides a lot of the security for pymine; it convert
# between 'client-space' structural s-representations of data as
# (approximately) specified in the protomine API, and the
# Django-internal model-based m-representations; the reason for doing
# this is partly philosophic - that there should be a clearly defined
# breakpoint between the two worlds, and this is it; if we just
# serialized models and slung them back and forth, the mine would be
# wedded to Django evermore, which is not a good thing.

# specialist types

def m2s_tagimplies(m, mname, s, sname):
    x = ' '.join([ x.name for x in m.implies.all() ])
    if x: s[sname] = x

def m2s_vurltags(m, mname, s, sname):
    x = ' '.join([ x.name for x in m.tags.all() ])
    if x: s[sname] = x

def m2s_itemtags(m, mname, s, sname):
    x = " ".join(x for x in itertools.chain([ i.name for i in self.tags.all() ],
                                            [ "for:%s" % i.name for i in self.item_for_relations.all() ],
                                            [ "not:%s" % i.name for i in self.item_not_relations.all() ]))
    if x: s[sname] = x

def m2s_relationinterests(m, mname, s, sname):
    x = " ".join(x for x in itertools.chain([ i.name for i in self.tags.all() ],
                                            [ "require:%s" % i.name for i in self.tags_required.all() ],
                                            [ "exclude:%s" % i.name for i in self.tags_excluded.all() ]))
    if x: s[sname] = x

# int types

def s2m_int(s, sname, m, mname):
    if sname in s: m[mname] = s[sname]

def m2s_int(m, mname, s, sname):
    x = getattr(m, mname)
    if x: s[sname] = x

# string types

def s2m_string(s, sname, m, mname):
    if sname in s: m[mname] = s[sname]

def m2s_string(m, mname, s, sname):
    x = getattr(m, mname)
    if x: s[sname] = x

# date types

def s2m_date(s, sname, m, mname):
    raise Exception, "---- NYI ----"

def m2s_date(m, mname, s, sname):
    x = getattr(m, mname)
    if x: s[sname] = x.isoformat()

# translation table

xtable = (
    #('structureName',          'model_attribute',  s2m_func,    m2s_func               ),
    ('commentBody',             'body',             s2m_string,  m2s_string             ),
    ('commentCreated',          'created',          s2m_date,    m2s_date               ),
    ('commentId',               'id',               s2m_int,     m2s_int                ),
    ('commentItem',             'item',             None,        None                   ),  #ForeignKey(Item)
    ('commentLastModified',     'last_modified',    s2m_date,    m2s_date               ),
    ('commentLikes',            'likes',            s2m_int,     m2s_int                ),
    ('commentRelation',         'relation',         None,        None                   ),  #ForeignKey(Relation)
    ('commentTitle',            'title',            s2m_string,  m2s_string             ),
    ('itemCreated',             'created',          s2m_date,    m2s_date               ),
    ('itemDescription',         'description',      s2m_string,  m2s_string             ),
    ('itemHideAfter',           'hide_after',       s2m_date,    m2s_date               ),
    ('itemHideBefore',          'hide_before',      s2m_date,    m2s_date               ),
    ('itemId',                  'id',               s2m_int,     m2s_int                ),
    ('itemLastModified',        'last_modified',    s2m_date,    m2s_date               ),
    ('itemName',                'name',             s2m_string,  m2s_string             ),
    ('itemStatus',              'status',           s2m_string,  m2s_string             ),
    ('itemTags',                'tags',             None,        m2s_itemtags           ),  #ManyToMany(Special)
    ('itemType',                'content_type',     s2m_string,  m2s_string             ),
    ('relationCallbackURL',     'url_callback',     s2m_string,  m2s_string             ),
    ('relationCreated',         'created',          s2m_date,    m2s_date               ),
    ('relationDescription',     'description',      s2m_string,  m2s_string             ),
    ('relationEmailAddress',    'email_address',    s2m_string,  m2s_string             ),
    ('relationEmbargoAfter',    'embargo_after',    s2m_date,    m2s_date               ),
    ('relationEmbargoBefore',   'embargo_before',   s2m_date,    m2s_date               ),
    ('relationHomepageURL',     'url_homepage',     s2m_string,  m2s_string             ),
    ('relationId',              'id',               s2m_int,     m2s_int                ),
    ('relationImageURL',        'url_image',        s2m_string,  m2s_string             ),
    ('relationInterests',       'interests',        None,        m2s_relationinterests  ),  #ManyToMany(Special)
    ('relationLastModified',    'last_modified',    s2m_date,    m2s_date               ),
    ('relationName',            'name',             s2m_string,  m2s_string             ),
    ('relationNetworkPattern',  'network_pattern',  s2m_string,  m2s_string             ),
    ('relationVersion',         'version',          s2m_int,     m2s_int                ),
    ('tagCreated',              'created',          s2m_date,    m2s_date               ),
    ('tagDescription',          'description',      s2m_string,  m2s_string             ),
    ('tagId',                   'id',               s2m_int,     m2s_int                ),
    ('tagImplies',              'implies',          None,        m2s_tagimplies         ),  #ManyToMany(Tag)
    ('tagLastModified',         'last_modified',    s2m_date,    m2s_date               ),
    ('tagName',                 'name',             s2m_string,  m2s_string             ),
    ('vurlCreated',             'created',          s2m_date,    m2s_date               ),
    ('vurlId',                  'id',               s2m_int,     m2s_int                ),
    ('vurlLastModified',        'last_modified',    s2m_date,    m2s_date               ),
    ('vurlLink',                'link',             s2m_string,  m2s_string             ),
    ('vurlName',                'name',             s2m_string,  m2s_string             ),
    ('vurlTags',                'tags',             None,        m2s_vurltags           ),  #ManyToMany(Tag)
    )

m2s_table = {}
m2s_table['comment'] = {}
m2s_table['item'] = {}
m2s_table['relation'] = {}
m2s_table['tag'] = {}
m2s_table['vurl'] = {}

s2m_table = {}
s2m_table['comment'] = {}
s2m_table['item'] = {}
s2m_table['relation'] = {}
s2m_table['tag'] = {}
s2m_table['vurl'] = {}

for (sname, mname, s2mfunc, m2sfunc) in xtable:

    for prefix in ('comment', 'item', 'relation', 'tag', 'vurl'):
        if sname.startswith(prefix):
            matched = True
            if m2sfunc: m2s_table[prefix][mname] = (m2sfunc, sname)
            if s2mfunc: s2m_table[prefix][sname] = (s2mfunc, mname)
            break
    else:
        raise Exception, "unrecognised prefix in xtable: " + sname

def model_to_structure(kind, m):
    s = {}

    print m2s_table[kind]

    for mname, (m2sfunc, sname) in m2s_table[kind].iteritems():
        m2sfunc(m, mname, s, sname)

    return s

def structure_to_model(kind, s, id=0):
    m = {}

    for sname, (s2mfunc, mname) in s2m_table[kind]:
        s2mfunc(s, sname, m, mname)

    if kind == 'item':
        return Item(**m)
    elif kind == 'tag':
        return Tag(**m)
    elif kind == 'relation':
        return Relation(**m)
    elif kind == 'comment':
        return Comment(**m)
    else:
        raise Exception, "unrecognised 'kind' in structure_to_model()"

def request_to_structure(kind, r):
    raise Exception, "---- NYI ----"

def request_to_model(kind, r, id=0):
    s = request_to_structure(kind, r)
    return structure_to_model(kind, s, id)
