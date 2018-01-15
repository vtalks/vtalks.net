from rest_framework import serializers

from .models import Channel


class ChannelSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    code = serializers.CharField(required=True, allow_blank=False, max_length=100)
    title = serializers.CharField(required=True, allow_blank=False, max_length=200)
    slug = serializers.SlugField(read_only=True)
    description = serializers.CharField(required=False, style={'base_template': 'textarea.html'})
    youtube_url = serializers.URLField(read_only=True)

    class Meta:
        model = Channel
        fields = ('id', 'code', 'title', 'slug', 'description', 'youtube_url')
