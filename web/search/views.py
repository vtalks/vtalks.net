from elasticsearch import Elasticsearch

from django.views.generic.list import ListView
from django.core.paginator import Paginator
from django.conf import settings

from .forms import SearchForm

from talks.models import Talk


class SearchTalksView(ListView):
    model = Talk
    template_name = 'search.html'
    paginate_by = settings.PAGE_SIZE

    def _search_talks_elasticsearch(self, q, page=1):
        page_start = 0
        if page > 1:
            page_start = self.paginate_by*(page-1)

        es = Elasticsearch([{
            'host': settings.ELASTICSEARCH['default']['HOSTNAME'],
            'port': settings.ELASTICSEARCH['default']['PORT'],
        }])

        results = es.search(index="talk",
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
                page = self.request.GET["page"]

            es_results_total, es_results_ids = self._search_talks_elasticsearch(query, page)
            search_results = Talk.published_objects.filter(pk__in=es_results_ids)
            paginator = Paginator(search_results, self.paginate_by)

            context['object_list'] = paginator.get_page(page)

        return context