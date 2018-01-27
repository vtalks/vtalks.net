from datetime import timedelta

from django.conf import settings

from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from taggit.managers import TaggableManager

from .decay import popularity

# Create your models here.


class Channel(models.Model):
    code = models.CharField(max_length=100, unique=True, default=None)
    title = models.CharField(max_length=200, default=None)
    slug = models.SlugField(max_length=200, unique=True, default=None)
    description = models.TextField(blank=True)
    created = models.DateTimeField('date created', default=timezone.now)
    updated = models.DateTimeField('date updated', default=timezone.now)

    @property
    def youtube_url(self):
        url = ""
        if self.code:
            url = "https://www.youtube.com/channel/{:s}".format(self.code)
        return url

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
        get_latest_by = ["-created"]
        ordering = ['-created']


class Playlist(models.Model):
    code = models.CharField(max_length=100, unique=True, default=None)
    title = models.CharField(max_length=200, default=None)
    slug = models.SlugField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True)
    created = models.DateTimeField('date created', default=timezone.now)
    updated = models.DateTimeField('date updated', default=timezone.now)

    # External URLs

    @property
    def youtube_url(self):
        url = ""
        if self.code:
            url = "https://www.youtube.com/playlist?list={:s}".format(self.code)
        return url

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
            if Playlist.objects.filter(slug=self.slug).count() > 0:
                self.slug = "{:s}-{:s}".format(self.slug, self.code)
        super(Playlist, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Playlist"
        verbose_name_plural = "Playlists"
        get_latest_by = ["-created"]
        ordering = ['-created']


class Talk(models.Model):
    code = models.CharField(max_length=25, unique=True, default=None)
    title = models.CharField(max_length=200, default=None)
    description = models.TextField()
    channel = models.ForeignKey(Channel, on_delete=models.DO_NOTHING)
    playlist = models.ForeignKey(Playlist, blank=True, null=True, on_delete=models.DO_NOTHING, default=None)
    slug = models.SlugField(max_length=200, unique=True, default=None)
    tags = TaggableManager(blank=True)
    duration = models.DurationField(default=timedelta())
    youtube_view_count = models.IntegerField('youtube view count', default=0)
    youtube_like_count = models.IntegerField('youtube like count', default=0)
    youtube_dislike_count = models.IntegerField('youtube dislike count', default=0)
    youtube_favorite_count = models.IntegerField('youtube favorite count', default=0)
    view_count = models.IntegerField('view count', default=0)
    like_count = models.IntegerField('like count', default=0)
    dislike_count = models.IntegerField('dislike count', default=0)
    favorite_count = models.IntegerField('favorite count', default=0)
    wilsonscore_rank = models.FloatField('wilson score rank', default=0)
    hacker_hot = models.FloatField('hackernews hot rank', default=0)
    created = models.DateTimeField('date created', default=timezone.now)
    updated = models.DateTimeField('date updated', default=timezone.now)

    # Thumbnails

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

    # External URLs

    @property
    def youtube_url(self):
        url = ""
        if self.code:
            url = "https://www.youtube.com/watch?v={:s}".format(self.code)
        return url

    # Total statistics

    @property
    def total_view_count(self):
        return self.youtube_view_count + self.view_count

    @property
    def total_like_count(self):
        return self.youtube_like_count + self.like_count

    @property
    def total_favorite_count(self):
        return self.youtube_favorite_count + self.favorite_count

    @property
    def total_dislike_count(self):
        return self.youtube_dislike_count + self.dislike_count

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Overrides save method.

        If it is a new object (it has the property 'id' as null on saving)
        generates an slug string from the title.
        In case two different talks but with the same title we append the code
        as suffix to the slug to prevent unique slugs for each element on the
        database.

        Also calculates the new ranking for the talk.
        """

        # check for repeated slugs
        if not self.id:
            # generate slug from title
            self.slug = slugify(self.title)
            # check if the generated slug is already being used and, in such
            # case we append the code to it.
            if Talk.objects.filter(slug=self.slug).count() > 0:
                self.slug = "{:s}-{:s}".format(self.slug, self.code)

        # calculate raking
        wilsonscore_rank = popularity.wilson_score(self.total_like_count, self.total_dislike_count)
        self.wilsonscore_rank = wilsonscore_rank

        hacker_hot = popularity.hacker_hot(self.total_view_count, self.created)
        self.hacker_hot = hacker_hot

        super(Talk, self).save(*args, **kwargs)

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
        verbose_name = "Talk Like"
        verbose_name_plural = "Talks Likes"
        get_latest_by = "-created"
        ordering = ['-created']


class TalkFavorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    talk = models.ForeignKey('Talk', default=1, on_delete=models.CASCADE)
    created = models.DateTimeField('date created', default=timezone.now)

    class Meta:
        verbose_name = "Talk Favorite"
        verbose_name_plural = "Talks Favorites"
        get_latest_by = "-created"
        ordering = ['-created']