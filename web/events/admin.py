from django.contrib import admin

from .models import Event
from .models import Edition

# Register your models here.


class EditionItemInline(admin.StackedInline):
    model = Edition
    extra = 1


class EventAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'description', 'url', 'twitter')
        }),
        ('Metadata', {
            'classes': ('collapse',),
            'fields': ('created', 'updated'),
        }),
    )
    list_display = ('title', 'url', 'twitter', 'updated', 'editions_count')
    date_hierarchy = 'created'
    list_filter = ['created', 'updated']
    search_fields = ['title']
    ordering = ['-updated']
    prepopulated_fields = {"slug": ("title",)}
    inlines = [EditionItemInline]


admin.site.register(Event, EventAdmin)


class EditionAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'description', 'url', 'country', 'city', 'venue', 'event', 'event_start', 'event_end')
        }),
        ('Metadata', {
            'classes': ('collapse',),
            'fields': ('created', 'updated'),
        }),
    )
    list_display = ('title', 'event', 'event_start', 'event_end', 'updated')
    date_hierarchy = 'created'
    list_filter = ['created', 'updated']
    search_fields = ['title']
    ordering = ['-updated']
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Edition, EditionAdmin)
