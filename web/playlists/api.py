from rest_framework import viewsets

from .models import Playlist

from .serializers import PlaylistSerializer

from django_filters.rest_framework import DjangoFilterBackend


class PlaylistViewSet(viewsets.ModelViewSet):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('code',)
