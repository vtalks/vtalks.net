from datetime import datetime
from datetime import timedelta

from django.conf import settings

from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from taggit.managers import TaggableManager

from channels.models import Channel
from playlists.models import Playlist
from events.models import Edition

from .utils import parse_duration
from .mixins import Rankable

from .managers import PublishedTalkManager

# Create your models here.


class Talk(Rankable, models.Model):
    code = models.CharField(max_length=25, unique=True, default=None)
    title = models.CharField(max_length=200, default=None)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=200, unique=True, default=None)
    tags = TaggableManager(blank=True)
    duration = models.DurationField(default=timedelta())

    channel = models.ForeignKey(Channel, on_delete=models.DO_NOTHING)
    playlist = models.ForeignKey(Playlist, blank=True, null=True, on_delete=models.DO_NOTHING, default=None)

    youtube_view_count = models.IntegerField('youtube view count', default=0)
    youtube_like_count = models.IntegerField('youtube like count', default=0)
    youtube_dislike_count = models.IntegerField('youtube dislike count', default=0)
    youtube_favorite_count = models.IntegerField('youtube favorite count', default=0)

    view_count = models.IntegerField('view count', default=0)
    like_count = models.IntegerField('like count', default=0)
    dislike_count = models.IntegerField('dislike count', default=0)
    favorite_count = models.IntegerField('favorite count', default=0)

    event_edition = models.ForeignKey(Edition, blank=True, null=True, default=None, on_delete=models.DO_NOTHING)

    created = models.DateTimeField('date created', default=timezone.now)
    updated = models.DateTimeField('date updated', default=timezone.now)

    published = models.BooleanField('is published', default=True)

    # Managers

    objects = models.Manager()
    published_objects = PublishedTalkManager()

    # Thumbnails

    @property
    def default_thumb(self):
        """ Returns an URL of the default thumbnail of the video
        """
        if self.code is None:
            return ""
        return "https://i.ytimg.com/vi/{:s}/default.jpg".format(self.code)

    @property
    def medium_thumb(self):
        """ Returns an URL of the medium sized thumbnail of the video
        """
        if self.code is None:
            return ""
        return "https://i.ytimg.com/vi/{:s}/mqdefault.jpg".format(self.code)

    @property
    def high_thumb(self):
        """ Returns an URL of the high resolution thumbnail of the video
        """
        if self.code is None:
            return ""
        return "https://i.ytimg.com/vi/{:s}/hqdefault.jpg".format(self.code)

    @property
    def standard_thumb(self):
        """ Returns an URL of the standard size thumbnail of the video
        """
        if self.code is None:
            return ""
        return "https://i.ytimg.com/vi/{:s}/sddefault.jpg".format(self.code)

    @property
    def maxres_thumb(self):
        """ Returns an URL iof the maximum resolution thumbnail of the video
        """
        if self.code is None:
            return ""
        return "https://i.ytimg.com/vi/{:s}/maxresdefault.jpg".format(self.code)

    # External URLs

    @property
    def youtube_url(self):
        """ Returns a Youtube URL of the video
        """
        if self.code is None:
            return ""
        return "https://www.youtube.com/watch?v={:s}".format(self.code)

    # Total statistics

    @property
    def total_view_count(self):
        """ Returns the total amount of views of a video
        """
        return int(self.youtube_view_count) + int(self.view_count)

    @property
    def total_like_count(self):
        """ Returns the total amount of 'likes' of a video
        """
        return int(self.youtube_like_count) + int(self.like_count)

    @property
    def total_favorite_count(self):
        """ Returns the total amount of 'favorites' of a video
        """
        return int(self.youtube_favorite_count) + int(self.favorite_count)

    @property
    def total_dislike_count(self):
        """ Returns the total amount of 'dislikes' of a video
        """
        return int(self.youtube_dislike_count) + int(self.dislike_count)

    def update_video_model(self, youtube_video_data):
        """ Updates model's common properties
        """
        self.code = youtube_video_data["id"]
        if "snippet" in youtube_video_data:
            snippet = youtube_video_data["snippet"]
            if "title" in snippet:
                self.title = youtube_video_data["snippet"]["title"]
            if "description" in snippet:
                self.description = youtube_video_data["snippet"]["description"]
            if "publishedAt" in snippet:
                published_at = youtube_video_data["snippet"]["publishedAt"]
                datetime_published_at = datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%S.000Z")
                datetime_published_at = datetime_published_at.replace(tzinfo=timezone.utc)
                self.created = datetime_published_at
        if "contentDetails" in youtube_video_data:
            content_details = youtube_video_data["contentDetails"]
            if "duration" in content_details:
                self.duration = parse_duration(content_details["duration"])

    def update_video_tags(self, youtube_video_data):
        """ Updates tags associated to this model instance
        """
        tags = []
        if "snippet" in youtube_video_data:
            snippet = youtube_video_data["snippet"]
            if "tags" in snippet:
                tags += snippet["tags"]
        for tag in tags:
            self.tags.add(tag)

    def update_video_statistics(self, youtube_video_data):
        """ Updates youtube video statistics ( likes, dislikes, favorites and
        views )
        """
        if "statistics" in youtube_video_data:
            statistics = youtube_video_data["statistics"]
            if "viewCount" in statistics:
                self.youtube_view_count = statistics["viewCount"]
            if "likeCount" in statistics:
                self.youtube_like_count = statistics["likeCount"]
            if "dislikeCount" in statistics:
                self.youtube_dislike_count = statistics["dislikeCount"]
            if "favoriteCount" in statistics:
                self.youtube_favorite_count = statistics["favoriteCount"]

    def recalculate_video_sortrank(self):
        """ Recalculates sort and ranking values given model's statistics
        """
        # wilson score
        wilsonscore_rank = self.get_wilson_score(self.total_like_count,
                                                 self.total_dislike_count)
        self.wilsonscore_rank = wilsonscore_rank

        # hacker news hot
        votes = abs(self.total_like_count - self.total_dislike_count)
        hacker_hot = self.get_hacker_hot(votes, self.created)
        self.hacker_hot = hacker_hot

    # Override methods

    def save(self, *args, **kwargs):
        """Overrides save method.

        If it is a new object (it has the property 'id' as null on saving)
        generates an slug string from the title.
        In case two different talks but with the same title we append the code
        as suffix to the slug to prevent unique slugs for each element on the
        database.

        Also recalculates the sort ranking values for the talk.
        """

        # check for repeated slugs
        if not self.id:
            # generate slug from title
            self.slug = slugify(self.title)
            # check if the generated slug is already being used and, in such
            # case we append the code to it.
            if Talk.objects.filter(slug=self.slug).count() > 0:
                self.slug = "{:s}-{:s}".format(self.slug, self.code)

        self.updated = timezone.now()

        self.recalculate_video_sortrank()

        super(Talk, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """ Returns the absolute url for this video
        """
        return "/talk/{}/".format(self.slug)

    def __str__(self):
        """ Returns the string representation of this object
        """
        return self.title

    class Meta:
        verbose_name = "Talk"
        verbose_name_plural = "Talks"
        get_latest_by = "-created"
        ordering = ['-created']


class TalkLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    talk = models.ForeignKey('Talk', default=1, on_delete=models.CASCADE)
    created = models.DateTimeField('date created', default=timezone.now)

    class Meta:
        unique_together = ('user', 'talk')
        verbose_name = "Talk Like"
        verbose_name_plural = "Talks Likes"
        get_latest_by = "-created"
        ordering = ['-created']


class TalkDislike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    talk = models.ForeignKey('Talk', default=1, on_delete=models.CASCADE)
    created = models.DateTimeField('date created', default=timezone.now)

    class Meta:
        unique_together = ('user', 'talk')
        verbose_name = "Talk Dislike"
        verbose_name_plural = "Talks Dislikes"
        get_latest_by = "-created"
        ordering = ['-created']


class TalkFavorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    talk = models.ForeignKey('Talk', default=1, on_delete=models.CASCADE)
    created = models.DateTimeField('date created', default=timezone.now)

    class Meta:
        unique_together = ('user', 'talk')
        verbose_name = "Talk Favorite"
        verbose_name_plural = "Talks Favorites"
        get_latest_by = "-created"
        ordering = ['-created']


class TalkWatch(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    talk = models.ForeignKey('Talk', default=1, on_delete=models.CASCADE)
    created = models.DateTimeField('date created', default=timezone.now)

    class Meta:
        unique_together = ('user', 'talk')
        verbose_name = "Talk Watch"
        verbose_name_plural = "Talks Watches"
        get_latest_by = "-created"
        ordering = ['-created']