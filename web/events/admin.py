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
            'fields': ('title', 'slug', 'description', 'url')
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
    prepopulated_fields = {"slug": ("title",)}
    inlines = [EditionItemInline]


admin.site.register(Event, EventAdmin)


class EditionAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'description', 'url', 'venue', 'event', 'event_start', 'event_end')
        }),
        ('Metadata', {
            'classes': ('collapse',),
            'fields': ('created', 'updated'),
        }),
    )
    list_display = ('title', 'event', 'event_start', 'event_end')
    date_hierarchy = 'created'
    list_filter = ['created', 'updated']
    search_fields = ['title']
    ordering = ['-created']
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Edition, EditionAdmin)
