from django.contrib import admin

from .models import Channel
from .models import Playlist
from .models import Talk

# Register your models here.


class ChannelAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('code', 'slug', 'title', 'description')
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
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Channel, ChannelAdmin)


class PlaylistAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('code', 'title', 'description')
        }),
        ('Youtube', {
            'fields': (),
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


admin.site.register(Playlist, PlaylistAdmin)


class TalkAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('code', 'slug', 'title', 'description', 'tags'),
        }),
        ('Youtube', {
            'fields': ('youtube_url', 'channel', 'playlist', 'duration'),
        }),
        ('Thumbnails', {
            'classes': ('collapse',),
            'fields': ('default_thumb', 'medium_thumb', 'high_thumb',
                       'standard_thumb', 'maxres_thumb'),
        }),
        ('Statistics', {
            'classes': ('collapse',),
            'fields': ('view_count', 'like_count', 'dislike_count'),
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
                       'view_count', 'like_count', 'dislike_count', 'duration')
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Talk, TalkAdmin)
