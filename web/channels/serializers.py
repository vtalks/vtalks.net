from rest_framework import serializers

from django.utils import timezone

from .models import Channel


class ChannelSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    code = serializers.CharField(required=True, allow_blank=False, max_length=100)
    title = serializers.CharField(required=True, allow_blank=False, max_length=200)
    slug = serializers.SlugField(read_only=True)
    description = serializers.CharField(required=False, style={'base_template': 'textarea.html'})
    youtube_url = serializers.URLField(read_only=True)
    created = serializers.DateTimeField(default=timezone.now)
    updated = serializers.DateTimeField(default=timezone.now)

    class Meta:
        model = Channel
        fields = '__all__'
        read_only_fields = ('id', 'slug', 'youtube_url')
