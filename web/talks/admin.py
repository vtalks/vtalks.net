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
        ('Youtube Data', {
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
        ('Youtube Data', {
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


admin.site.register(Playlist, PlaylistAdmin)


class TalkAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('code', 'slug', 'title', 'description', 'tags'),
        }),
        ('Youtube Data', {
            'fields': ('youtube_url', 'channel', 'playlist', 'duration'),
        }),
        ('Youtube Statistics', {
            'fields': ('youtube_view_count', 'youtube_like_count',
                       'youtube_dislike_count', 'youtube_favorite_count'),
        }),
        ('Local Statistics', {
            'fields': ('view_count', 'like_count', 'dislike_count',
                       'favorite_count'),
        }),
        ('Rank', {
            'fields': ('wilsonscore_rank', 'hacker_hot'),
        }),
        ('Thumbnails', {
            'classes': ('collapse',),
            'fields': ('default_thumb', 'medium_thumb', 'high_thumb',
                       'standard_thumb', 'maxres_thumb'),
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
                       'duration')
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Talk, TalkAdmin)
