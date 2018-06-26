import math
import json

from elasticsearch import Elasticsearch

from django.views.generic.detail import DetailView
from django.conf import settings

from search.forms import SearchForm

from taggit.models import Tag
from talks.models import Talk


class DetailTagView(DetailView):
    model = Tag
    template_name = 'details-tag.html'
    paginate_by = settings.PAGE_SIZE

    def build_elastic_search_query_dsl(self, tag, page=None):
        """ Builds an elastic search query DSL for this topic
        """
        query = {
            "query": {"bool": {"must": []}}
        }

        query["query"]["bool"]["must"].append({
            "match": {"tags": tag.name},
        })
        if page:
            page_start = 0
            if page > 1:
                page_start = settings.PAGE_SIZE * (page - 1)
            query["from"] = page_start
            query["size"] = settings.PAGE_SIZE
        return json.dumps(query)

    def get_talks_elasticsearch(self, tag, page=None):
        """ Get talks from this Topic from ElasticSearch
        """
        es = Elasticsearch([{
            'host': settings.ELASTICSEARCH['default']['HOSTNAME'],
            'port': settings.ELASTICSEARCH['default']['PORT'],
        }])

        elastic_search_index = "vtalks"
        results = es.search(index=elastic_search_index,
                            body=self.build_elastic_search_query_dsl(tag, page))
        results_total = results['hits']['total']
        results_ids = [ids['_id'] for ids in results['hits']['hits']]
        return results_total, results_ids

    def get_context_data(self, **kwargs):
        context = super(DetailTagView, self).get_context_data(**kwargs)

        search_form = SearchForm()
        context['search_form'] = search_form

        slug = self.kwargs['slug']
        tag = Tag.objects.get(slug=slug)
        context['object'] = tag

        page = 1
        if "page" in self.kwargs:
            page = self.kwargs["page"]
        es_results_total, es_results_ids = self.get_talks_elasticsearch(tag, page=page)
        search_results = Talk.published_objects.filter(pk__in=es_results_ids)

        num_pages = math.ceil(es_results_total / self.paginate_by)
        pagination = {}
        pagination['is_paginated'] = True if es_results_total > self.paginate_by else False
        pagination['number'] = page
        pagination['num_pages'] = num_pages
        pagination['has_previous'] = True if page > 1 else False
        pagination['previous_page_number'] = page - 1
        pagination['has_next'] = True if page < num_pages else False
        pagination['next_page_number'] = page + 1
        context['pagination'] = pagination
        context['object_list'] = search_results

        return context