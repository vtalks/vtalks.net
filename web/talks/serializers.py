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
        read_only_fields = ('id', 'slug', 'youtube_url')


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
        read_only_fields = ('id', 'slug', 'youtube_url')


class TalkSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    code = serializers.CharField(required=True, allow_blank=False, max_length=100)
    title = serializers.CharField(required=True, allow_blank=False, max_length=200)
    slug = serializers.SlugField(read_only=True)
    description = serializers.CharField(required=False, style={'base_template': 'textarea.html'})
    duration = serializers.DurationField()
    youtube_url = serializers.URLField(read_only=True)
    default_thumb = serializers.URLField(read_only=True)
    medium_thumb = serializers.URLField(read_only=True)
    high_thumb = serializers.URLField(read_only=True)
    standard_thumb = serializers.URLField(read_only=True)
    maxres_thumb = serializers.URLField(read_only=True)
    view_count = serializers.IntegerField(default=0)
    like_count = serializers.IntegerField(default=0)
    dislike_count = serializers.IntegerField(default=0)
    favorite_count = serializers.IntegerField(default=0)
    youtube_view_count = serializers.IntegerField(default=0)
    youtube_like_count = serializers.IntegerField(default=0)
    youtube_dislike_count = serializers.IntegerField(default=0)
    youtube_favorite_count = serializers.IntegerField(default=0)
    total_view_count = serializers.IntegerField(default=0, read_only=True)
    total_like_count = serializers.IntegerField(default=0, read_only=True)
    total_dislike_count = serializers.IntegerField(default=0, read_only=True)
    total_favorite_count = serializers.IntegerField(default=0, read_only=True)
    wilsonscore_rank = serializers.FloatField(default=0)
    hacker_hot = serializers.FloatField(default=0)
    created = serializers.DateTimeField(default=timezone.now)
    updated = serializers.DateTimeField(default=timezone.now)

    class Meta:
        model = Talk
        fields = '__all__'
        read_only_fields = ('id', 'slug', 'youtube_url',
                            'default_thumb', 'medium_thumb', 'high_thumb', 'standard_thumb', 'maxres_thumb',
                            'total_view_count', 'total_like_count', 'total_dislike_count', 'total_favorite_count')
