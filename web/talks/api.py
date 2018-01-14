from tastypie.resources import ModelResource
from .models import Channel
from .models import Playlist


class ChannelResource(ModelResource):

    class Meta:
        queryset = Channel.objects.all()
        resource_name = 'channel'


class PlaylistResource(ModelResource):

    class Meta:
        queryset = Playlist.objects.all()
        resource_name = 'playlist'
