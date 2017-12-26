from django.views.generic import TemplateView

from django.contrib.postgres.search import SearchVector
from django.contrib.postgres.search import SearchQuery
from django.contrib.postgres.search import SearchRank

from django.conf import settings
from django.core.paginator import Paginator

from .models import Talk
from .forms import SearchForm

# Create your views here.


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        search_form = SearchForm()
        context['search_form'] = search_form

        latest_talks = Talk.objects.all().order_by('-created')[:3]
        context['latest_talks'] = latest_talks

        return context


class SearchView(TemplateView):
    template_name = 'search.html'

    def _search_talks(self, q):
        vector = SearchVector('title', weight='A') + SearchVector('description', weight='B')
        query = SearchQuery(q)
        rank = SearchRank(vector, query)
        search_results = Talk.objects.annotate(rank=rank)
        # Filter by minimum rank
        search_results = search_results.filter(rank__gte=0.1)
        # Sort by rank (descendant)
        search_results = search_results.order_by('-rank')
        # Paginate results
        p = Paginator(search_results, settings.PAGE_SIZE)
        return p

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)

        page = 1
        if "page" in self.request.GET:
            page = self.request.GET["page"]
        search_form = SearchForm(self.request.GET)
        if search_form.is_valid():
            q = search_form.cleaned_data['q']
            search_results_paginator = self._search_talks(q)
            context['search_query'] = q
            context['search_results'] = search_results_paginator.get_page(page)
        context['search_form'] = search_form

        return context
