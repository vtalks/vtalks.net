from django.contrib import admin

from .models import Channel

# Register your models here.


class ChannelAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('code', 'title', 'slug', 'description')
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
    list_display = ['title', 'updated']
    list_filter = ['created', 'updated']
    search_fields = ['title', 'code']
    ordering = ['-updated']
    readonly_fields = ('youtube_url',)
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Channel, ChannelAdmin)
