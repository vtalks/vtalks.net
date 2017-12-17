from django.contrib import admin

from django.utils.html import format_html

from .models import Channel
from .models import Talk

# Register your models here.


class ChannelAdmin(admin.ModelAdmin):
    list_filter = ['created', 'updated']
    search_fields = ['title']
    ordering = ['-created', '-updated']
    readonly_fields = ('channel_url',)

    def channel_url(self, instance):
        """Returns the youtube URL of the channel
        """
        return format_html(
            '<a href="https://www.youtube.com/channel/{}">https://www.youtube.com/channel/{}</a>',
            instance.code, instance.code)

admin.site.register(Channel, ChannelAdmin)


class TalkAdmin(admin.ModelAdmin):
    list_display = ('title', 'channel')
    list_filter = ['created', 'updated']
    search_fields = ['title']
    ordering = ['-created', '-updated']
    readonly_fields = ('video_url',)

    def video_url(self, instance):
        """Returns the youtube URL of the video
        """
        return format_html(
            '<a href="https://www.youtube.com/watch?v={}">https://www.youtube.com/watch?v={}</a>',
            instance.code, instance.code)

admin.site.register(Talk, TalkAdmin)
