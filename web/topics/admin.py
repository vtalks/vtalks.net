from django.contrib import admin

from dal import autocomplete

from .models import Topic
from .forms import TopicForm

# Register your models here.


class TopicAdmin(admin.ModelAdmin):
    form = TopicForm

    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'description', 'tags')
        }),
        ('Status', {
            'fields': ('published',),
        }),
        ('Properties', {
            'fields': ('logo_url',),
        }),
        ('Metadata', {
            'classes': ('collapse',),
            'fields': ('created', 'updated'),
        }),
    )
    
    list_display = ('title', 'parent_topic', 'subtopics_count', 'talks_count', 'updated')
    list_filter = ['created', 'updated']
    search_fields = ['title',]
    date_hierarchy = 'created'
    ordering = ['-updated']
    readonly_fields = ('logo_url', 'talks_count', 'subtopics_count')
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Topic, TopicAdmin)