from rest_framework import serializers

from django.utils import timezone

from .models import Channel
from .models import Playlist
from .models import Talk


class ChannelSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    code = serializers.CharField(required=True, allow_blank=False, max_length=100)
    title = serializers.CharField(required=True, allow_blank=False, max_length=200)
    slug = serializers.SlugField(read_only=True)
    description = serializers.CharField(required=False, style={'base_template': 'textarea.html'})
    youtube_url = serializers.URLField(read_only=True)

    class Meta:
        model = Channel
        fields = '__all__'


class PlaylistSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    code = serializers.CharField(required=True, allow_blank=False, max_length=100)
    title = serializers.CharField(required=True, allow_blank=False, max_length=200)
    slug = serializers.SlugField(read_only=True)
    description = serializers.CharField(required=False, style={'base_template': 'textarea.html'})
    youtube_url = serializers.URLField(read_only=True)

    class Meta:
        model = Playlist
        fields = '__all__'


class TalkSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    code = serializers.CharField(required=True, allow_blank=False, max_length=100)
    title = serializers.CharField(required=True, allow_blank=False, max_length=200)
    slug = serializers.SlugField(read_only=True)
    description = serializers.CharField(required=False, style={'base_template': 'textarea.html'})
    youtube_url = serializers.URLField(read_only=True)
    view_count = serializers.IntegerField(default=0, read_only=True)
    like_count = serializers.IntegerField(default=0, read_only=True)
    dislike_count = serializers.IntegerField(default=0, read_only=True)
    favorite_count = serializers.IntegerField(default=0, read_only=True)
    youtube_view_count = serializers.IntegerField(default=0, read_only=True)
    youtube_like_count = serializers.IntegerField(default=0, read_only=True)
    youtube_dislike_count = serializers.IntegerField(default=0, read_only=True)
    youtube_favorite_count = serializers.IntegerField(default=0, read_only=True)
    total_view_count = serializers.IntegerField(default=0, read_only=True)
    total_like_count = serializers.IntegerField(default=0, read_only=True)
    total_dislike_count = serializers.IntegerField(default=0, read_only=True)
    total_favorite_count = serializers.IntegerField(default=0, read_only=True)
    wilsonscore_rank = serializers.FloatField(default=0, read_only=True)
    hacker_hot = serializers.FloatField(default=0, read_only=True)
    duration = serializers.DurationField(read_only=True)
    created = serializers.DateTimeField(default=timezone.now, read_only=True)
    updated = serializers.DateTimeField(default=timezone.now, read_only=True)

    class Meta:
        model = Talk
        fields = '__all__'
