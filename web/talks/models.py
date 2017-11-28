from django.db import models

# Create your models here.

class Talk(models.Model):
    code = models.CharField(max_length=25, unique=True, null=False, blank=False, default=None)
    title = models.CharField(max_length=200, null=False, blank=False, default=None)
    created = models.DateTimeField('date created')
    updated = models.DateTimeField('date updated')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Talk"
        verbose_name_plural = "Talks"
        get_latest_by = "-created"
        ordering = ['-created', '-updated']
