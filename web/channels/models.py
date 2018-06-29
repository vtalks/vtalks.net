from datetime import datetime

from django.db import models
from django.utils import timezone
from django.utils.text import slugify

# Create your models here.


class Channel(models.Model):
    code = models.CharField(max_length=100, unique=True, default=None)
    title = models.CharField(max_length=200, default=None)
    slug = models.SlugField(max_length=200, unique=True, default=None)
    description = models.TextField(blank=True)

    created = models.DateTimeField('date created', default=timezone.now)
    updated = models.DateTimeField('date updated', default=timezone.now)

    # External URLs

    @property
    def youtube_url(self):
        """ Returns a Youtube URL of the channel
        """
        url = ""
        if self.code:
            url = "https://www.youtube.com/channel/{:s}".format(self.code)
        return url

    def update_playlist_model(self, youtube_channel_data):
        """ Updates model's common properties
        """
        self.code = youtube_channel_data["id"]
        if "snippet" in youtube_channel_data:
            snippet = youtube_channel_data["snippet"]
            if "title" in snippet:
                self.title = youtube_channel_data["snippet"]["title"]
            if "description" in snippet:
                self.description = youtube_channel_data["snippet"]["description"]
            if "publishedAt" in snippet:
                published_at = youtube_channel_data["snippet"]["publishedAt"]
                datetime_published_at = datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%S.000Z")
                datetime_published_at = datetime_published_at.replace(tzinfo=timezone.utc)
                self.created = datetime_published_at

    # Override methods

    def save(self, *args, **kwargs):
        """Overrides save method.

        If it is a new object (it has the property 'id' as null on saving)
        generates an slug string from the title.
        In case two different channels but with the same title we append the code
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

        self.updated = timezone.now()

        super(Channel, self).save(*args, **kwargs)

    def __str__(self):
        """ Returns the string representation of this object
        """
        return self.title

    class Meta:
        verbose_name = "Channel"
        verbose_name_plural = "Channels"
        get_latest_by = ["-created"]
        ordering = ['-created']
