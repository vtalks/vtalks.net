from django.contrib import admin

from .models import Playlist

# Register your models here.


class PlaylistAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('code', 'slug', 'title', 'description')
        }),
        ('Youtube Data', {
            'fields': ('youtube_url', 'channel'),
        }),
        ('Metadata', {
            'classes': ('collapse',),
            'fields': ('created', 'updated'),
        }),
    )
    date_hierarchy = 'created'
    list_filter = ['created', 'updated']
    list_display = ['title', 'updated']
    search_fields = ['title', 'code']
    ordering = ['-updated']
    readonly_fields = ('youtube_url',)
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Playlist, PlaylistAdmin)