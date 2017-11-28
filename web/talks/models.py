from django.db import models

# Create your models here.

class Talk(models.Model):
    code = models.CharField(max_length=25, unique=True, null=False, blank=False, default=None)
    title = models.CharField(max_length=200, null=False, blank=False, default=None)
