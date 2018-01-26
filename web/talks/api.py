from random import randint

from rest_framework import viewsets
from rest_framework import views
from rest_framework.response import Response

from django.db.models.aggregates import Count

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


class RandomTalkView(views.APIView):

    def get(self, request, format=None):
        count = Talk.objects.aggregate(count=Count('id'))['count']
        if count == 0:
            return Response(None)

        random_index = randint(0, count - 1)
        talk = Talk.objects.all()[random_index]

        serializer = TalkSerializer(talk, many=False)
        return Response(serializer.data)
