from django.contrib import admin

from .models import Topic

# Register your models here.


class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'created')
    list_filter = ['created',]
    date_hierarchy = 'created'
    ordering = ['-created']
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Topic, TopicAdmin)