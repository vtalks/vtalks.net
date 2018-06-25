from rest_framework import serializers
from taggit_serializer.serializers import TagListSerializerField
from taggit_serializer.serializers import TaggitSerializer

from django.utils import timezone

from talks.models import Talk


class TalkSerializer(TaggitSerializer, serializers.ModelSerializer):
    id = serializers.IntegerField()
    code = serializers.CharField()
    title = serializers.CharField()
    description = serializers.CharField()
    duration = serializers.DurationField()
    view_count = serializers.IntegerField(default=0)
    like_count = serializers.IntegerField(default=0)
    dislike_count = serializers.IntegerField(default=0)
    favorite_count = serializers.IntegerField(default=0)
    youtube_view_count = serializers.IntegerField(default=0)
    youtube_like_count = serializers.IntegerField(default=0)
    youtube_dislike_count = serializers.IntegerField(default=0)
    youtube_favorite_count = serializers.IntegerField(default=0)
    total_view_count = serializers.IntegerField(default=0)
    total_like_count = serializers.IntegerField(default=0)
    total_dislike_count = serializers.IntegerField(default=0)
    total_favorite_count = serializers.IntegerField(default=0)
    wilsonscore_rank = serializers.FloatField(default=0)
    hacker_hot = serializers.FloatField(default=0)
    tags = TagListSerializerField()
    created = serializers.DateTimeField(default=timezone.now)
    updated = serializers.DateTimeField(default=timezone.now)

    class Meta:
        model = Talk
        fields = '__all__'
