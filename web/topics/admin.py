from django.contrib import admin

from dal import autocomplete

from .models import Topic
from .forms import TopicForm

# Register your models here.


class TopicAdmin(admin.ModelAdmin):
    form = TopicForm

    list_display = ('title', 'created', 'parent_topic', 'talks_count')
    list_filter = ['created',]
    date_hierarchy = 'created'
    ordering = ['-created']
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Topic, TopicAdmin)