from rest_framework import viewsets

from .models import Channel

from .serializers import ChannelSerializer

from django_filters.rest_framework import DjangoFilterBackend


class ChannelViewSet(viewsets.ModelViewSet):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('code',)
