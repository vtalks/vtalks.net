from tastypie.resources import NamespacedModelResource
from tastypie.authentication import ApiKeyAuthentication

from .models import Channel
from .models import Playlist
from .models import Talk


class ChannelResource(NamespacedModelResource):
    class Meta:
        queryset = Channel.objects.all()
        resource_name = 'channel'
        authentication = ApiKeyAuthentication()


class PlaylistResource(NamespacedModelResource):
    class Meta:
        queryset = Playlist.objects.all()
        resource_name = 'playlist'
        authentication = ApiKeyAuthentication()


class TalkResource(NamespacedModelResource):
    class Meta:
        queryset = Talk.objects.all()
        resource_name = 'talk'
        authentication = ApiKeyAuthentication()
