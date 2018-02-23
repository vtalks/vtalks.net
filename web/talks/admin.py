from django.contrib import admin

from .models import Playlist
from .models import Talk
from .models import TalkLike
from .models import TalkDislike
from .models import TalkFavorite
from .models import TalkWatch

# Register your models here.


class PlaylistAdmin(admin.ModelAdmin):
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
    ordering = ['-created']
    readonly_fields = ('youtube_url',)
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Playlist, PlaylistAdmin)


class TalkAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('code', 'slug', 'title', 'description', 'tags'),
        }),
        ('EVent Data', {
            'fields': ('event_edition',),
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

    list_display = ('title', 'channel')
    list_filter = ['created', 'updated']
    search_fields = ['title']
    ordering = ['-created']
    readonly_fields = ('default_thumb', 'medium_thumb', 'high_thumb',
                       'standard_thumb', 'maxres_thumb', 'youtube_url',
                       'duration')
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Talk, TalkAdmin)


class TalkLikeAdmin(admin.ModelAdmin):
    list_display = ('created', 'user', 'talk')
    list_filter = ['created',]
    date_hierarchy = 'created'
    ordering = ['-created']


admin.site.register(TalkLike, TalkLikeAdmin)


class TalkDislikeAdmin(admin.ModelAdmin):
    list_display = ('created', 'user', 'talk')
    list_filter = ['created',]
    date_hierarchy = 'created'
    ordering = ['-created']


admin.site.register(TalkDislike, TalkDislikeAdmin)


class TalkFavoriteAdmin(admin.ModelAdmin):
    list_display = ('created', 'user', 'talk')
    list_filter = ['created',]
    date_hierarchy = 'created'
    ordering = ['-created']


admin.site.register(TalkFavorite, TalkFavoriteAdmin)


class TalkWatchAdmin(admin.ModelAdmin):
    list_display = ('created', 'user', 'talk')
    list_filter = ['created',]
    date_hierarchy = 'created'
    ordering = ['-created']


admin.site.register(TalkWatch, TalkWatchAdmin)