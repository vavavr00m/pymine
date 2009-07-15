from pymine.frontend.models import Tag, Relation, Item, Comment
from django.contrib import admin

class TagAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name']}), 
        ('Implying Tags', {'fields': ['implied'], 'classes': ['collapse']}), 
        ('Advanced', {'fields': ['implied_cache'], 'classes': ['collapse']}), 
        ]

class RelationAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'version', 'description', 'interests']}), 
        ('Advanced Tags', {'fields': ['interests_exclude', 'interests_require'], 'classes': ['collapse']}), 
        ('Contact Information', {'fields': ['email_address', 'url_homepage', 'url_image', 'url_callback']}), 
        ('Access Control', {'fields': ['embargo_before', 'embargo_after', 'ip_address_pattern'], 'classes': ['collapse']}), 
        ]

class ItemAdmin(admin.ModelAdmin):
    fieldsets = [
        ]

class CommentAdmin(admin.ModelAdmin):
    fieldsets = [
        ]


admin.site.register(Tag, TagAdmin)
admin.site.register(Relation, RelationAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Comment, CommentAdmin)
