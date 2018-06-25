import json
from django.db import models

from django.utils import timezone
from django.utils.text import slugify

from taggit.models import Tag
from talks.models import Talk


# Create your models here.


class Topic(models.Model):
    title = models.CharField(max_length=200, default=None)
    slug = models.SlugField(max_length=200, unique=True, default=None)
    description = models.TextField(blank=True)
    tags = models.ManyToManyField(Tag)
    elastic_search_query_dsl = models.TextField(blank=True)
    created = models.DateTimeField('date created', default=timezone.now)
    updated = models.DateTimeField('date updated', default=timezone.now)

    # Properties

    @property
    def talks_count(self):
        """ Get the number of talks on this Topic
        """
        return self.get_talks(count=None).count()

    def build_elastic_search_query_dsl(self):
        """ Builds an elastic search query DSL for this topic
        """
        query = {
            "query": {"bool": {"should": []}}
        }
        tag_names = set(tag.name for tag in self.tags.all())
        for tag_name in tag_names:
            query["query"]["bool"]["should"].append({
                "match": {"tags": tag_name}}
            )
        return json.dumps(query)

    def get_talks(self, count=3):
        """ Get talks from this Topic
        """
        tags_slugs = set(tag.slug for tag in self.tags.all())
        tagged_talks = Talk.published_objects.filter(tags__slug__in=tags_slugs).order_by('-wilsonscore_rank', '-created').distinct()
        if count:
            tagged_talks = tagged_talks[:count]
        return tagged_talks

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

        self.elastic_search_query_dsl = self.build_elastic_search_query_dsl()
        self.updated = timezone.now()

        super(Topic, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Topic"
        verbose_name_plural = "Topics"
        get_latest_by = ["-created"]
        ordering = ['-created']
