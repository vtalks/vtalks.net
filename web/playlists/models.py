from datetime import datetime

from django.db import models

from django.utils import timezone
from django.utils.text import slugify

from channels.models import Channel

from playlists.events import publish_playlist_event

# Create your models here.


class Playlist(models.Model):
    code = models.CharField(max_length=100, unique=True, default=None)
    title = models.CharField(max_length=200, default=None)
    slug = models.SlugField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True)
    channel = models.ForeignKey(Channel, blank=True, null=True, on_delete=models.DO_NOTHING, default=None)

    created = models.DateTimeField('date created', default=timezone.now)
    updated = models.DateTimeField('date updated', default=timezone.now)

    # External URLs

    @property
    def youtube_url(self):
        """ Returns a Youtube URL of the playlist
        """
        url = ""
        if self.code:
            url = "https://www.youtube.com/playlist?list={:s}".format(self.code)
        return url

    # Override methods

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

        self.updated = timezone.now()

        super(Playlist, self).save(*args, **kwargs)

        # Send pipeline.talk event to NATS
        publish_playlist_event(self.youtube_url)

    def __str__(self):
        """ Returns the string representation of this object
        """
        return self.title

    class Meta:
        verbose_name = "Playlist"
        verbose_name_plural = "Playlists"
        get_latest_by = ["-created"]
        ordering = ['-created']
