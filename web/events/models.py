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
        verbose_name_plural = "Event"
        get_latest_by = ["-created"]
        ordering = ['-created']
