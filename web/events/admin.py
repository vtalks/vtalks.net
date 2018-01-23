from django.contrib import admin

from .models import Event

# Register your models here.


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


admin.site.register(Event, EventAdmin)
