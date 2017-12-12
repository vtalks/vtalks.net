from django.db import models
from django.utils import timezone
from django.utils.text import slugify

# Create your models here.


class Channel(models.Model):
    code = models.CharField(max_length=25, unique=True, null=False, blank=False, default=None)
    title = models.CharField(max_length=200, null=False, blank=False, default=None)
    created = models.DateTimeField('date created', default=timezone.now)
    updated = models.DateTimeField('date updated', default=timezone.now)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Channel"
        verbose_name_plural = "Channels"
        get_latest_by = "-created"
        ordering = ['-created', '-updated']


class Talk(models.Model):
    code = models.CharField(max_length=25, unique=True, null=False, blank=False, default=None)
    title = models.CharField(max_length=200, null=False, blank=False, default=None)
    description = models.TextField()
    channel = models.ForeignKey('Channel', on_delete=models.CASCADE, null=False, blank=False, default=None)
    slug = models.SlugField(max_length=200, unique=True, blank=False)
    viewCount = models.IntegerField(null=False, blank=False, default=0)
    likeCount = models.IntegerField(null=False, blank=False, default=0)
    dislikeCount = models.IntegerField(null=False, blank=False, default=0)
    favoriteCount = models.IntegerField(null=False, blank=False, default=0)
    created = models.DateTimeField('date created', default=timezone.now)
    updated = models.DateTimeField('date updated', default=timezone.now)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Do not update the slug if it is updating
        if not self.id:
            self.slug = slugify(self.title)
            if Talk.objects.filter(slug=self.slug).count() > 0:
                self.slug = self.slug + "-" + self.code
        super(Talk, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Talk"
        verbose_name_plural = "Talks"
        get_latest_by = "-created"
        ordering = ['-created', '-updated']
