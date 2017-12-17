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
            'fields': ('youtubeURL',),
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
    readonly_fields = ('youtubeURL',)

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
            'fields': ('youtubeURL',),
        }),
        ('Thumbnails', {
            'classes': ('collapse',),
            'fields': ('defaultThumb', 'mediumThumb', 'highThumb',
                       'standardThumb', 'maxresThumb'),
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
    readonly_fields = ('defaultThumb', 'mediumThumb', 'highThumb',
                       'standardThumb', 'maxresThumb', 'youtubeURL',
                       'viewCount', 'likeCount', 'dislikeCount',)
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(Talk, TalkAdmin)
