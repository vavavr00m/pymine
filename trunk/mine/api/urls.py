from django.conf.urls.defaults import *
import views as api

# Regarding:
# 'POST': api.update_comment_key
# 'POST': api.update_item_key
# 'POST': api.update_relation_key
# 'POST': api.update_tag_key
# See http://is.gd/1PsBm or http://tinyurl.com/na9qej
# "A method for massively cutting UPDATE/HTTP-PUT methods in complex ReST APIs"

# Regarding:
# 'POST': api.create_item_data (rather than PUT/UPDATE)
# ...frankly I can't be bothered to do PUT logic for 1 method

urlpatterns = patterns('',
    (r'^config.(?P<fmt>(xml|json|py))$',
     api.DISPATCH, {'GET': api.read_config, 'POST': api.create_config}),
    (r'^item.(?P<fmt>(xml|json|py))$',
     api.DISPATCH, {'GET': api.read_item_list, 'POST': api.create_item}),
    (r'^item/(?P<iid>\d+)$',
     api.DISPATCH, {'GET': api.read_item_data, 'POST': api.create_item_data}),
    (r'^item/(?P<iid>\d+).(?P<fmt>(xml|json|py))$',
     api.DISPATCH, {'DELETE': api.delete_item, 'GET': api.read_item}),
    (r'^item/(?P<iid>\d+)/(?P<cid>\d+).(?P<fmt>(xml|json|py))$',
     api.DISPATCH, {'DELETE': api.delete_comment, 'GET': api.read_comment}),
    (r'^item/(?P<iid>\d+)/(?P<cid>\d+)/key.(?P<fmt>(xml|json|py))$',
     api.DISPATCH, {'POST': api.create_comment_key}),
    (r'^item/(?P<iid>\d+)/(?P<cid>\d+)/key/(?P<key>\w+).(?P<fmt>(xml|json|py))$',
     api.DISPATCH, {'DELETE': api.delete_comment_key, 'GET': api.read_comment_key, 'POST': api.create_comment_key}),
    (r'^item/(?P<iid>\d+)/clone.(?P<fmt>(xml|json|py))$',
     api.DISPATCH, {'GET': api.read_clone_list, 'POST': api.create_clone}),
    (r'^item/(?P<iid>\d+)/comment.(?P<fmt>(xml|json|py))$',
     api.DISPATCH, {'GET': api.read_comment_list, 'POST': api.create_comment}),
    (r'^item/(?P<iid>\d+)/key.(?P<fmt>(xml|json|py))$',
     api.DISPATCH, {'POST': api.create_item_key}),
    (r'^item/(?P<iid>\d+)/key/(?P<key>\w+).(?P<fmt>(xml|json|py))$',
     api.DISPATCH, {'DELETE': api.delete_item_key, 'GET': api.read_item_key, 'POST': api.create_item_key}),
    (r'^relation.(?P<fmt>(xml|json|py))$',
     api.DISPATCH, {'GET': api.read_relation_list, 'POST': api.create_relation}),
    (r'^relation/(?P<rid>\d+).(?P<fmt>(xml|json|py))$',
     api.DISPATCH, {'DELETE': api.delete_relation, 'GET': api.read_relation}),
    (r'^relation/(?P<rid>\d+)/key.(?P<fmt>(xml|json|py))$',
     api.DISPATCH, {'POST': api.create_relation_key}),
    (r'^relation/(?P<rid>\d+)/key/(?P<key>\w+).(?P<fmt>(xml|json|py))$',
     api.DISPATCH, {'DELETE': api.delete_relation_key, 'GET': api.read_relation_key, 'POST': api.create_relation_key}),
    (r'^select/item.(?P<fmt>(xml|json|py))$',
     api.DISPATCH, {'GET': api.read_select_item}),
    (r'^select/relation.(?P<fmt>(xml|json|py))$',
     api.DISPATCH, {'GET': api.read_select_relation}),
    (r'^select/tag.(?P<fmt>(xml|json|py))$',
     api.DISPATCH, {'GET': api.read_select_tag}),
    (r'^tag.(?P<fmt>(xml|json|py))$',
     api.DISPATCH, {'GET': api.read_tag_list, 'POST': api.create_tag}),
    (r'^tag/(?P<tid>\d+).(?P<fmt>(xml|json|py))$',
     api.DISPATCH, {'DELETE': api.delete_tag, 'GET': api.read_tag}),
    (r'^tag/(?P<tid>\d+)/key.(?P<fmt>(xml|json|py))$',
     api.DISPATCH, {'POST': api.create_tag_key}),
    (r'^tag/(?P<tid>\d+)/key/(?P<key>\w+).(?P<fmt>(xml|json|py))$',
     api.DISPATCH, {'DELETE': api.delete_tag_key, 'GET': api.read_tag_key, 'POST': api.create_tag_key}),
    (r'^url/(?P<rid>\d+).(?P<fmt>(xml|json|py))$',
     api.DISPATCH, {'GET': api.read_encode_minekey1}),
    (r'^url/(?P<rid>\d+)/(?P<iid>\d+).(?P<fmt>(xml|json|py))$',
     api.DISPATCH, {'GET': api.read_encode_minekey2}),
    (r'^url/(?P<rid>\d+)/(?P<rvsn>\d+)/(?P<iid>\d+).(?P<fmt>(xml|json|py))$',
     api.DISPATCH, {'GET': api.read_encode_minekey3}),
    (r'^version.(?P<fmt>(xml|json|py))$',
     api.DISPATCH, {'GET': api.read_version}),
)
