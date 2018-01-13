from datetime import timedelta

from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from taggit.managers import TaggableManager

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


class Playlist(models.Model):
    code = models.CharField(max_length=100, unique=True, default=None)
    title = models.CharField(max_length=200, default=None)
    description = models.TextField(blank=True)
    created = models.DateTimeField('date created', default=timezone.now)
    updated = models.DateTimeField('date updated', default=timezone.now)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Playlist"
        verbose_name_plural = "Playlists"
        get_latest_by = "-created"
        ordering = ['-created', '-updated']


class Talk(models.Model):
    code = models.CharField(max_length=25, unique=True, default=None)
    title = models.CharField(max_length=200, default=None)
    description = models.TextField()
    channel = models.ForeignKey(Channel, on_delete=models.DO_NOTHING)
    playlist = models.ForeignKey(Playlist, blank=True, null=True, on_delete=models.DO_NOTHING, default=None)
    slug = models.SlugField(max_length=200, unique=True, default=None)
    tags = TaggableManager(blank=True)
    duration = models.DurationField(default=timedelta())
    view_count = models.IntegerField('view count', default=0)
    like_count = models.IntegerField('like count', default=0)
    dislike_count = models.IntegerField('dislike count', default=0)
    wilsonscore_rank = models.FloatField('wilson score rank', default=0)
    hacker_hot = models.FloatField('hackernews hot rank', default=0)
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
