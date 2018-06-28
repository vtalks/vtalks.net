import math
from elasticsearch import Elasticsearch

from django.views.generic.list import ListView
from django.conf import settings

from .forms import SearchForm

from talks.models import Talk


class SearchTalksView(ListView):
    model = Talk
    template_name = 'search.html'
    paginate_by = settings.PAGE_SIZE

    def _search_talks_elasticsearch(self, q, page=1, sort="relevance"):
        page_start = 0
        if page > 1:
            page_start = self.paginate_by*(page-1)

        es = Elasticsearch([{
            'host': settings.ELASTICSEARCH['default']['HOSTNAME'],
            'port': settings.ELASTICSEARCH['default']['PORT'],
        }])

        if sort == 'date':
            sort = 'created'
        elif sort == 'popularity':
            sort = 'wilsonscore_rank'
        else:
            sort = '_score'

        elastic_search_index = "vtalks"
        results = es.search(index=elastic_search_index,
                            body={
                                "query": {
                                    "multi_match": {
                                        "query": q,
                                        "fields": ["title", "description"],
                                    },
                                },
                                "from": page_start,
                                "size": self.paginate_by,
                                "_source": ["id"],
                                "sort": {sort: {"order": "desc"}}
                            })
        results_total = results['hits']['total']
        results_ids = [ids['_id'] for ids in results['hits']['hits']]

        return results_total, results_ids

    def get_context_data(self, **kwargs):
        context = super(SearchTalksView, self).get_context_data(**kwargs)

        search_form = SearchForm(self.request.GET)
        context['search_form'] = search_form

        if search_form.is_valid():
            query = search_form.cleaned_data['q']
            context['search_query'] = query

            page = 1
            if "page" in self.request.GET:
                page = int(self.request.GET["page"])

            sort = "relevance"
            if "sort" in self.request.GET:
                sort = self.request.GET["sort"]

            es_results_total, es_results_ids = self._search_talks_elasticsearch(query, page, sort)
            search_results = Talk.published_objects.filter(pk__in=es_results_ids)

            num_pages = math.ceil(es_results_total / self.paginate_by)
            pagination={}
            pagination['is_paginated'] = True if es_results_total > self.paginate_by else False
            pagination['number'] = page
            pagination['num_pages'] = num_pages
            pagination['has_previous'] = True if page > 1 else False
            pagination['previous_page_number'] = page - 1
            pagination['has_next'] = True if page < num_pages else False
            pagination['next_page_number'] = page + 1
            context['pagination'] = pagination
            context['sort'] = sort
            context['object_list'] = search_results

        return context
