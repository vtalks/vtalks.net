import json

from elasticsearch import Elasticsearch

from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.conf import settings

from taggit.models import Tag
from talks.models import Talk


# Create your models here.


class Topic(models.Model):
    title = models.CharField(max_length=200, default=None)
    slug = models.SlugField(max_length=200, unique=True, default=None)
    description = models.TextField(blank=True)
    parent_topic = models.ForeignKey("self", blank=True, null=True, default=None, on_delete=models.DO_NOTHING)
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

    @property
    def talks_count_elasticsearch(self):
        """ Get the number of talks on this Topic (from ElasticSearch)
        """
        es = Elasticsearch([{
            'host': settings.ELASTICSEARCH['default']['HOSTNAME'],
            'port': settings.ELASTICSEARCH['default']['PORT'],
        }])

        elastic_search_index = "vtalks"
        results = es.search(index=elastic_search_index,
                            body=self.elastic_search_query_dsl)
        results_total = results['hits']['total']
        return results_total

    def build_elastic_search_query_dsl(self, page=None, sort=None):
        """ Builds an elastic search query DSL for this topic
        """
        query = {
            "query": {"bool": {"should": []}}
        }
        tag_names = set(tag.name for tag in self.tags.all())
        for tag_name in tag_names:
            query["query"]["bool"]["should"].append({
                "match": {"tags": tag_name},
            })
        if page:
            page_start = 0
            if page > 1:
                page_start = settings.PAGE_SIZE * (page - 1)
            query["from"] = page_start
            query["size"] = settings.PAGE_SIZE
        if sort:
            if sort == 'date':
                sort = 'created'
            elif sort == 'popularity':
                sort = 'wilsonscore_rank'
            else:
                sort = '_score'
            query["sort"] = {sort: {"order": "desc"}}
        return json.dumps(query)

    def get_talks(self, count=3):
        """ Get talks from this Topic
        """
        results_total, results_ids = self.get_talks_elasticsearch()
        if count:
            results_ids = results_ids[:count]
        topic_talks = Talk.published_objects.filter(pk__in=results_ids)
        return topic_talks

    def get_talks_elasticsearch(self, page=None, sort=None):
        """ Get talks from this Topic from ElasticSearch
        """
        es = Elasticsearch([{
            'host': settings.ELASTICSEARCH['default']['HOSTNAME'],
            'port': settings.ELASTICSEARCH['default']['PORT'],
        }])

        elastic_search_index = "vtalks"
        results = es.search(index=elastic_search_index,
                            body=self.build_elastic_search_query_dsl(page=page, sort=sort))
        results_total = results['hits']['total']
        results_ids = [ids['_id'] for ids in results['hits']['hits']]
        return results_total, results_ids

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

        if not self.elastic_search_query_dsl:
            self.elastic_search_query_dsl = self.build_elastic_search_query_dsl()
            self.save()

    class Meta:
        verbose_name = "Topic"
        verbose_name_plural = "Topics"
        get_latest_by = ["-created"]
        ordering = ['-created']
