from django.contrib import admin

from .models import Talk

# Register your models here.

class TalkAdmin(admin.ModelAdmin):
    list_display = ('title', 'created', 'updated')
    list_filter = ['created']
    search_fields = ['title']

admin.site.register(Talk, TalkAdmin)
