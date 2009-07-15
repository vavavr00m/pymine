from pymine.frontend.models import Tag, Relation, Item, Comment
from django.contrib import admin

class TagAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name']}), 
        ('Implying Tags', {'fields': ['implies'], 'classes': ['collapse']}), 
        ('Advanced', {'fields': ['cached_implications'], 'classes': ['collapse']}), 
        ]

class RelationAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'version', 'description', 'tags']}), 
        ('Advanced Tags', {'fields': ['tags_excluded', 'tags_required'], 'classes': ['collapse']}), 
        ('Contact Information', {'fields': ['email_address', 'url_homepage', 'url_image', 'url_callback']}), 
        ('Access Control', {'fields': ['embargo_before', 'embargo_after', 'network_pattern'], 'classes': ['collapse']}), 
        ]

class ItemAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'status', 'content_type', 'description', 'tags']}), 
        ('Advanced Tags', {'fields': ['item_for_relations', 'item_not_relations'], 'classes': ['collapse']}), 
        ('Access Control', {'fields': ['hide_before', 'hide_after'], 'classes': ['collapse']}), 
        ]

class CommentAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['title', 'body', 'likes_this']}), 
        ('Advanced', {'fields': ['item', 'relation']}), 
        ]

admin.site.register(Tag, TagAdmin)
admin.site.register(Relation, RelationAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Comment, CommentAdmin)
