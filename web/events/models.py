from django.db import models

from django.utils import timezone
from django.utils.text import slugify

# Create your models here.


class Event(models.Model):
    title = models.CharField(max_length=200, default=None)
    slug = models.SlugField(max_length=200, unique=True, default=None)
    description = models.TextField(blank=True)
    url = models.URLField(blank=True)
    twitter = models.CharField(max_length=200, null=True, blank=True, default=None)
    created = models.DateTimeField('date created', default=timezone.now)
    updated = models.DateTimeField('date updated', default=timezone.now)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Overrides save method.

        If it is a new object (it has the property 'id' as null on saving)
        generates an slug string from the title.
        In case two different events but with the same title we append the code
        as suffix to the slug to prevent unique slugs for each element on the
        database.
        """
        if not self.id:
            # generate slug from title
            self.slug = slugify(self.title)
            # check if the generated slug is already being used and, in such
            # case we append the code to it.
            count = Event.objects.filter(slug=self.slug).count()
            if count > 0:
                self.slug = "{:s}-{:d}".format(self.slug, count)

        self.updated = timezone.now()

        super(Event, self).save(*args, **kwargs)

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
    country = models.CharField(max_length=200, null=True, blank=True, default=None)
    city = models.CharField(max_length=200, null=True, blank=True, default=None)
    venue = models.CharField(max_length=400, null=True, blank=True, default=None)
    event_start = models.DateField('start', null=True, blank=True)
    event_end = models.DateField('end', null=True, blank=True)
    created = models.DateTimeField('date created', default=timezone.now)
    updated = models.DateTimeField('date updated', default=timezone.now)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Overrides save method.

        If it is a new object (it has the property 'id' as null on saving)
        generates an slug string from the title.
        In case two different events but with the same title we append the code
        as suffix to the slug to prevent unique slugs for each element on the
        database.
        """
        if not self.id:
            # generate slug from title
            self.slug = slugify(self.title)
            # check if the generated slug is already being used and, in such
            # case we append the code to it.
            count = Edition.objects.filter(slug=self.slug).count()
            if count > 0:
                self.slug = "{:s}-{:d}".format(self.slug, count)
        super(Edition, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Edition"
        verbose_name_plural = "Editions"
        get_latest_by = ["-created"]
        ordering = ['-created']