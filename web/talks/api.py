from rest_framework import viewsets

from .models import Channel
from .models import Playlist
from .models import Talk

from .serializers import ChannelSerializer
from .serializers import PlaylistSerializer
from .serializers import TalkSerializer


class ChannelViewSet(viewsets.ModelViewSet):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer


class PlaylistViewSet(viewsets.ModelViewSet):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer


class TalkViewSet(viewsets.ModelViewSet):
    queryset = Talk.objects.all()
    serializer_class = TalkSerializer
