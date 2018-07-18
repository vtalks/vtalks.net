from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from taggit.models import Tag
from talks.models import Talk
from topics.search import search_talks_by_topic

from topics.managers import PublishedTopicManager


# Create your models here.


class Topic(models.Model):
    title = models.CharField(max_length=200, default=None)
    slug = models.SlugField(max_length=200, unique=True, default=None)
    description = models.TextField(blank=True)
    parent_topic = models.ForeignKey("self", blank=True, null=True, default=None, on_delete=models.DO_NOTHING)
    tags = models.ManyToManyField(Tag)
    created = models.DateTimeField('date created', default=timezone.now)
    updated = models.DateTimeField('date updated', default=timezone.now)

    published = models.BooleanField('is published', default=True)

    # Managers

    objects = models.Manager()
    published_objects = PublishedTopicManager()

    # Properties

    @property
    def talks_count(self):
        """ Get the number of talks on this Topic (from ElasticSearch)
        """
        results_total, es_results_ids = search_talks_by_topic(self)
        return results_total

    @property
    def subtopics(self):
        """ Get a list of subtopics for this Topic
        """
        topics = Topic.published_objects.filter(parent_topic=self)
        return topics[:4]

    def get_talks(self, count=3):
        """ Get talks from this Topic
        """
        results_total, results_ids = search_talks_by_topic(self)
        topic_talks = Talk.published_objects.filter(pk__in=results_ids)
        if count:
            topic_talks = topic_talks[:count]
        return topic_talks

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Overrides save method.

        If it is a new object (it has the property 'id' as null on saving)
        generates an slug string from the title.
        In case two different channels but with the same title we append the code
        as suffix to the slug to prevent unique slugs for each element on the
        database.
        """
        if not self.id:
            # generate slug from title
            self.slug = slugify(self.title)
            # check if the generated slug is already being used and, in such
            # case we append the code to it.
            count = Topic.objects.filter(slug=self.slug).count()
            if count > 0:
                self.slug = "{:s}-{:s}".format(self.slug, str(count))

        self.updated = timezone.now()

        super(Topic, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Topic"
        verbose_name_plural = "Topics"
        get_latest_by = ["-created"]
        ordering = ['-created']
