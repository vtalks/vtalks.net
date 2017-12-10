from django.db import models

from django.utils.text import slugify


class Channel(models.Model):
    code = models.CharField(max_length=25, unique=True, null=False, blank=False, default=None)
    title = models.CharField(max_length=200, null=False, blank=False, default=None)
    description = models.TextField()
    created = models.DateTimeField('date created')
    updated = models.DateTimeField('date updated')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Talk"
        verbose_name_plural = "Talks"
        get_latest_by = "-created"
        ordering = ['-created', '-updated']


class Talk(models.Model):
    YOUTUBE = 'Y'
    VIMEO = 'V'
    VIDEO_TYPE_CHOICES = (
        (YOUTUBE, 'Youtube'),
        (VIMEO, 'Vimeo'),
    )
    vtype = models.CharField(max_length=1, choices=VIDEO_TYPE_CHOICES, null=False, blank=False, default=YOUTUBE)
    code = models.CharField(max_length=25, unique=True, null=False, blank=False, default=None)
    title = models.CharField(max_length=200, null=False, blank=False, default=None)
    description = models.TextField()
    channel = models.CharField(max_length=25, default=None)
    slug = models.SlugField(max_length=200, unique=True, blank=False)
    created = models.DateTimeField('date created')
    updated = models.DateTimeField('date updated')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
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
