from django.db import models

from django.utils import timezone

# Create your models here.


class Event(models.Model):
    title = models.CharField(max_length=200, default=None)
    slug = models.SlugField(max_length=200, unique=True, default=None)
    description = models.TextField(blank=True)
    url = models.URLField(blank=True)
    created = models.DateTimeField('date created', default=timezone.now)
    updated = models.DateTimeField('date updated', default=timezone.now)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"
        get_latest_by = ["-created"]
        ordering = ['-created']


class Edition(models.Model):
    event = models.ForeignKey('Event', on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default=None)
    slug = models.SlugField(max_length=200, unique=True, default=None)
    description = models.TextField(blank=True)
    url = models.URLField(blank=True)
    venue = models.CharField(max_length=400, null=True, blank=True, default=None)
    event_start = models.DateField('start', null=True, blank=True)
    event_end = models.DateField('end', null=True, blank=True)
    created = models.DateTimeField('date created', default=timezone.now)
    updated = models.DateTimeField('date updated', default=timezone.now)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Edition"
        verbose_name_plural = "Editions"
        get_latest_by = ["-created"]
        ordering = ['-created']