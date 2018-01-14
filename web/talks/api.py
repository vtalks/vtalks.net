from tastypie.resources import NamespacedModelResource

from .models import Channel
from .models import Playlist
from .models import Talk


class ChannelResource(NamespacedModelResource):
    class Meta:
        queryset = Channel.objects.all()
        resource_name = 'channel'


class PlaylistResource(NamespacedModelResource):
    class Meta:
        queryset = Playlist.objects.all()
        resource_name = 'playlist'


class TalkResource(NamespacedModelResource):
    class Meta:
        queryset = Talk.objects.all()
        resource_name = 'talk'
