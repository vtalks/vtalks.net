from rest_framework import viewsets

from talks.models import Channel
from talks.serializers import ChannelSerializer

# Create your views here.


class ChannelViewSet(viewsets.ModelViewSet):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
