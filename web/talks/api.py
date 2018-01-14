from tastypie.resources import ModelResource
from .models import Channel


class ChannelResource(ModelResource):

    class Meta:
        queryset = Channel.objects.all()
        resource_name = 'channel'
