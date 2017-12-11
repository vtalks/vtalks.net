from django.contrib import admin


from .models import Channel
from .models import Talk

# Register your models here.


class ChannelAdmin(admin.ModelAdmin):
    pass


admin.site.register(Channel, ChannelAdmin)


class TalkAdmin(admin.ModelAdmin):
    pass


admin.site.register(Talk, TalkAdmin)
