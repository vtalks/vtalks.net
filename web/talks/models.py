from datetime import timedelta

from django.conf import settings

from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from taggit.managers import TaggableManager

from channels.models import Channel
from playlists.models import Playlist
from events.models import Edition

from talks.mixins import Rankable
from talks.managers import PublishedTalkManager

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