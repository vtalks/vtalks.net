import requests

from datetime import timedelta

from urllib.parse import urlsplit
from urllib.parse import parse_qs

from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.core.management.base import CommandError

from taggit.managers import TaggableManager

# Create your models here.


class Channel(models.Model):
    code = models.CharField(max_length=25, unique=True, default=None)
    title = models.CharField(max_length=200, default=None)
    slug = models.SlugField(max_length=200, unique=True, default=None)
    description = models.TextField(blank=True)
    created = models.DateTimeField('date created', default=timezone.now)
    updated = models.DateTimeField('date updated', default=timezone.now)

    @property
    def youtube_url(self):
        return "https://www.youtube.com/channel/{:s}".format(self.code)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Overrides save method.

        If it is a new object (it has the property 'id' as null on saving)
        generates an slug string from the title.
        In case two different talks but with the same title we append the code
        as suffix to the slug to prevent unique slugs for each element on the
        database.
        """
        if not self.id:
            # generate slug from title
            self.slug = slugify(self.title)
            # check if the generated slug is already being used and, in such
            # case we append the code to it.
            if Channel.objects.filter(slug=self.slug).count() > 0:
                self.slug = "{:s}-{:s}".format(self.slug, self.code)
        super(Channel, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Channel"
        verbose_name_plural = "Channels"
        get_latest_by = "-created"
        ordering = ['-created', '-updated']


class Talk(models.Model):
    code = models.CharField(max_length=25, unique=True, default=None)
    title = models.CharField(max_length=200, default=None)
    description = models.TextField()
    channel = models.ForeignKey(Channel, on_delete=models.DO_NOTHING)
    slug = models.SlugField(max_length=200, unique=True, default=None)
    tags = TaggableManager(blank=True)
    duration = models.DurationField(default=timedelta())
    view_count = models.IntegerField('view count', default=0)
    like_count = models.IntegerField('like count', default=0)
    dislike_count = models.IntegerField('dislike count', default=0)
    created = models.DateTimeField('date created', default=timezone.now)
    updated = models.DateTimeField('date updated', default=timezone.now)
    
    @property
    def default_thumb(self):
        return "https://i.ytimg.com/vi/{:s}/default.jpg".format(self.code)

    @property
    def medium_thumb(self):
        return "https://i.ytimg.com/vi/{:s}/mqdefault.jpg".format(self.code)

    @property
    def high_thumb(self):
        return "https://i.ytimg.com/vi/{:s}/hqdefault.jpg".format(self.code)

    @property
    def standard_thumb(self):
        return "https://i.ytimg.com/vi/{:s}/sddefault.jpg".format(self.code)

    @property
    def maxres_thumb(self):
        return "https://i.ytimg.com/vi/{:s}/maxresdefault.jpg".format(self.code)

    @property
    def youtube_url(self):
        return "https://www.youtube.com/watch?v={:s}".format(self.code)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Overrides save method.

        If it is a new object (it has the property 'id' as null on saving)
        generates an slug string from the title.
        In case two different talks but with the same title we append the code
        as suffix to the slug to prevent unique slugs for each element on the
        database.
        """
        if not self.id:
            # generate slug from title
            self.slug = slugify(self.title)
            # check if the generated slug is already being used and, in such
            # case we append the code to it.
            if Talk.objects.filter(slug=self.slug).count() > 0:
                self.slug = "{:s}-{:s}".format(self.slug, self.code)
        super(Talk, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Talk"
        verbose_name_plural = "Talks"
        get_latest_by = "-created"
        ordering = ['-created', '-updated']


def get_video_code(url):
    query = urlsplit(url).query
    params = parse_qs(query)
    if "v" not in params:
        raise CommandError('Invalid url "%s"' % url)
    video_code = params["v"][0]
    return video_code


def fetch_channel_data(youtube_api_key, channel_code):
    channel_url = "https://www.googleapis.com/youtube/v3/channels"
    payload = {'id': channel_code,
               'part': 'snippet,contentDetails',
               'key': youtube_api_key}
    resp = requests.get(channel_url, params=payload)
    if resp.status_code != 200:
        raise CommandError('Error fetching channel data "%s"' % resp.status_code)
    response_json = resp.json()
    channel_data = None
    if len(response_json["items"]) > 0:
        channel_data = response_json["items"][0]
    return channel_data


def fetch_video_data(youtube_api_key, video_code):
    video_url = "https://www.googleapis.com/youtube/v3/videos"
    payload = {'id': video_code,
               'part': 'snippet,contentDetails,statistics,topicDetails,status,recordingDetails,player,localizations,liveStreamingDetails',
               'key': youtube_api_key}
    resp = requests.get(video_url, params=payload)
    if resp.status_code != 200:
        raise CommandError('Error fetching video data "%s"' % resp.status_code)
    response_json = resp.json()
    video_data = None
    if len(response_json["items"]) > 0:
        video_data = response_json["items"][0]
    return video_data


def fetch_playlist_items(youtube_api_key, playlist_code):
    channel_url = "https://www.googleapis.com/youtube/v3/playlistItems"
    payload = {'playlistId': playlist_code,
               'maxResults': 50,
               'part': 'snippet',
               'key': youtube_api_key}
    resp = requests.get(channel_url, params=payload)
    if resp.status_code != 200:
        if resp.status_code == 404:
            return []
        else:
            raise CommandError('Error fetching playlist items "%s"' % resp.status_code)
    response_json = resp.json()
    videos_id_list = []
    data_json = response_json["items"]
    for item in data_json:
        videos_id_list.append(item["snippet"]["resourceId"]["videoId"])
    return videos_id_list
