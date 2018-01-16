from rest_framework import viewsets

from .models import Channel
from .models import Playlist

from .serializers import ChannelSerializer
from .serializers import PlaylistSerializer


class ChannelViewSet(viewsets.ModelViewSet):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer


class PlaylistViewSet(viewsets.ModelViewSet):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
