from django.db import models


class PublishedTalkManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(published=True)