from django.db import models
from django.utils import timezone
from django.utils.text import slugify

# Create your models here.


class Channel(models.Model):
    """Channel model"""
    code = models.CharField(max_length=25, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    created = models.DateTimeField('date created', default=timezone.now)
    updated = models.DateTimeField('date updated', default=timezone.now)

    @property
    def youtube_url(self):
        if self.code == "":
            return "-"
        return "https://www.youtube.com/channel/{:s}".format(self.code)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Channel"
        verbose_name_plural = "Channels"
        get_latest_by = "-created"
        ordering = ['-created', '-updated']


class Talk(models.Model):
    """Talk model"""
    code = models.CharField(max_length=25, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    channel = models.ForeignKey(Channel, on_delete=models.DO_NOTHING)
    slug = models.SlugField(max_length=200, unique=True)
    tags = models.CharField(max_length=500, null=True, blank=True, default="")
    viewCount = models.IntegerField('view count', default=0)
    likeCount = models.IntegerField('like count', default=0)
    dislikeCount = models.IntegerField('dislike count', default=0)
    created = models.DateTimeField('date created', default=timezone.now)
    updated = models.DateTimeField('date updated', default=timezone.now)
    
    @property
    def default_thumb(self):
        if self.code == "":
            return "-"
        return "https://i.ytimg.com/vi/{:s}/default.jpg".format(self.code)

    @property
    def medium_thumb(self):
        if self.code == "":
            return "-"
        return "https://i.ytimg.com/vi/{:s}/mqdefault.jpg".format(self.code)

    @property
    def high_thumb(self):
        if self.code == "":
            return "-"
        return "https://i.ytimg.com/vi/{:s}/hqdefault.jpg".format(self.code)

    @property
    def standard_thumb(self):
        if self.code == "":
            return "-"
        return "https://i.ytimg.com/vi/{:s}/sddefault.jpg".format(self.code)

    @property
    def maxres_thumb(self):
        if self.code == "":
            return "-"
        return "https://i.ytimg.com/vi/{:s}/maxresdefault.jpg".format(self.code)

    @property
    def youtube_url(self):
        if self.code == "":
            return "-"
        return "https://www.youtube.com/watch?v={:s}".format(self.code)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Overrides save method.

        If it is a new object (it has the property 'id' as null on saving) generates an slug string from the title.
        In case two different talks but with the same title we append the code as suffix to the slug to prevent unique
        slugs for each element on the database.
        """
        if not self.id:
            # generate slug from title
            self.slug = slugify(self.title)
            # check if the generated slug is already being used, in such case we append the code to it.
            if Talk.objects.filter(slug=self.slug).count() > 0:
                self.slug = "{:s}-{:s}".format(self.slug, self.code)
        super(Talk, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Talk"
        verbose_name_plural = "Talks"
        get_latest_by = "-created"
        ordering = ['-created', '-updated']
