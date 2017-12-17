from django.contrib import admin

from django.utils.html import format_html

from .models import Channel
from .models import Talk

# Register your models here.


class ChannelAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('code', 'title', 'description')
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
    readonly_fields = ('channel_url',)

    def channel_url(self, instance):
        """Returns the youtube URL of the channel
        """
        return format_html(
            '<a href="https://www.youtube.com/channel/{}">https://www.youtube.com/channel/{}</a>',
            instance.code, instance.code)

admin.site.register(Channel, ChannelAdmin)


class TalkAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('code', 'slug', 'title', 'description', 'channel', 'tags'),
        }),
        ('Youtube', {
            'fields': ('video_url',),
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
    readonly_fields = ('video_url', 'viewCount', 'likeCount', 'dislikeCount')
    prepopulated_fields = {"slug": ("title",)}

    def video_url(self, instance):
        """Returns the youtube URL of the video
        """
        return format_html(
            '<a href="https://www.youtube.com/watch?v={}">https://www.youtube.com/watch?v={}</a>',
            instance.code, instance.code)

admin.site.register(Talk, TalkAdmin)
