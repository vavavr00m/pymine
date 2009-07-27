from django.conf.urls.defaults import *
from mine.views import REST
import views as api

# Regarding:
# 'POST': api.update_comment_key
# 'POST': api.update_item_key
# 'POST': api.update_relation_key
# 'POST': api.update_tag_key
# See http://is.gd/1PsBm or http://tinyurl.com/na9qej
# "A method for massively cutting UPDATE/HTTP-PUT methods in complex ReST APIs"

urlpatterns = patterns('',
    (r'^item/(?P<iid>\d+)$', # <-------------------- SPECIAL CASE
     REST, {'GET': api.read_item_data, 'POST': api.update_item_data, 'PUT': api.update_item_data }),

    (r'^config.(?P<fmt>(xml|json|html|txt))$',
     REST, {'GET': api.read_config, 'POST': api.create_config}),
    (r'^item.(?P<fmt>(xml|json|html|txt))$',
     REST, {'GET': api.read_item_list, 'POST': api.create_item}),
    (r'^item/(?P<iid>\d+).(?P<fmt>(xml|json|html|txt))$',
     REST, {'DELETE': api.delete_item, 'GET': api.read_item}),
    (r'^item/(?P<iid>\d+)/(?P<cid>\d+).(?P<fmt>(xml|json|html|txt))$',
     REST, {'DELETE': api.delete_comment, 'GET': api.read_comment}),
    (r'^item/(?P<iid>\d+)/(?P<cid>\d+)/key.(?P<fmt>(xml|json|html|txt))$',
     REST, {'POST': api.create_comment_key}),
    (r'^item/(?P<iid>\d+)/(?P<cid>\d+)/key/(?P<key>\w+).(?P<fmt>(xml|json|html|txt))$',
     REST, {'DELETE': api.delete_comment_key, 'GET': api.read_comment_key, 'POST': api.update_comment_key}),
    (r'^item/(?P<iid>\d+)/clone.(?P<fmt>(xml|json|html|txt))$',
     REST, {'GET': api.read_clone_list, 'POST': api.create_clone}),
    (r'^item/(?P<iid>\d+)/comment.(?P<fmt>(xml|json|html|txt))$',
     REST, {'GET': api.read_comment_list, 'POST': api.create_comment}),
    (r'^item/(?P<iid>\d+)/key.(?P<fmt>(xml|json|html|txt))$',
     REST, {'POST': api.create_item_key}),
    (r'^item/(?P<iid>\d+)/key/(?P<key>\w+).(?P<fmt>(xml|json|html|txt))$',
     REST, {'DELETE': api.delete_item_key, 'GET': api.read_item_key, 'POST': api.update_item_key}),
    (r'^relation.(?P<fmt>(xml|json|html|txt))$',
     REST, {'GET': api.read_relation_list, 'POST': api.create_relation}),
    (r'^relation/(?P<rid>\d+).(?P<fmt>(xml|json|html|txt))$',
     REST, {'DELETE': api.delete_relation, 'GET': api.read_relation}),
    (r'^relation/(?P<rid>\d+)/key.(?P<fmt>(xml|json|html|txt))$',
     REST, {'POST': api.create_relation_key}),
    (r'^relation/(?P<rid>\d+)/key/(?P<key>\w+).(?P<fmt>(xml|json|html|txt))$',
     REST, {'DELETE': api.delete_relation_key, 'GET': api.read_relation_key, 'POST': api.update_relation_key}),
    (r'^tag.(?P<fmt>(xml|json|html|txt))$',
     REST, {'GET': api.read_tag_list, 'POST': api.create_tag}),
    (r'^tag/(?P<tid>\d+).(?P<fmt>(xml|json|html|txt))$',
     REST, {'DELETE': api.delete_tag, 'GET': api.read_tag}),
    (r'^tag/(?P<tid>\d+)/key.(?P<fmt>(xml|json|html|txt))$',
     REST, {'POST': api.create_tag_key}),
    (r'^tag/(?P<tid>\d+)/key/(?P<key>\w+).(?P<fmt>(xml|json|html|txt))$',
     REST, {'DELETE': api.delete_tag_key, 'GET': api.read_tag_key, 'POST': api.update_tag_key}),
    (r'^version.(?P<fmt>(xml|json|html|txt))$',
     REST, {'GET': api.read_version}),
)
