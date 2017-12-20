from rest_framework import serializers

from .models import Channel

# Create your serializers here.


class ChannelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Channel
        fields = ('id', 'title', 'code', 'description', 'created', 'updated')
