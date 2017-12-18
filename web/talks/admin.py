from django.contrib import admin

from .models import Channel
from .models import Talk

# Register your models here.


class ChannelAdmin(admin.ModelAdmin):
    """Channel model admin
    """
    fieldsets = (
        (None, {
            'fields': ('code', 'title', 'description')
        }),
        ('Youtube', {
            'fields': ('youtube_url',),
        }),
        ('Metadata', {
            'classes': ('collapse',),
            'fields': ('created', 'updated'),
        }),
    )
    date_hierarchy = 'created'
    list_filter = ['created', 'updated']
    search_fields = ['title']
    ordering = ['-updated', '-created']
    readonly_fields = ('youtube_url',)


admin.site.register(Channel, ChannelAdmin)


class TalkAdmin(admin.ModelAdmin):
    """Talk model admin
    """
    fieldsets = (
        (None, {
            'fields': ('code', 'slug', 'title', 'description', 'channel',
                       'tags'),
        }),
        ('Youtube', {
            'fields': ('youtube_url',),
        }),
        ('Thumbnails', {
            'classes': ('collapse',),
            'fields': ('default_thumb', 'medium_thumb', 'high_thumb',
                       'standard_thumb', 'maxres_thumb'),
        }),
        ('Statistics', {
            'classes': ('collapse',),
            'fields': ('viewCount', 'likeCount', 'dislikeCount'),
        }),
        ('Metadata', {
            'classes': ('collapse',),
            'fields': ('created', 'updated'),
        }),
    )
    date_hierarchy = 'created'
    list_display = ('title', 'channel')
    list_filter = ['created', 'updated']
    search_fields = ['title']
    ordering = ['-updated', '-created']
    readonly_fields = ('default_thumb', 'medium_thumb', 'high_thumb',
                       'standard_thumb', 'maxres_thumb', 'youtube_url',
                       'viewCount', 'likeCount', 'dislikeCount',)
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Talk, TalkAdmin)
