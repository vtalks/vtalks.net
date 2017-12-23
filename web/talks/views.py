from django.views.generic import TemplateView

from django.contrib.postgres.search import SearchVector
from django.contrib.postgres.search import SearchQuery
from django.contrib.postgres.search import SearchRank

from .models import Talk
from .forms import SearchForm

# Create your views here.


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        search_form = SearchForm()

        context['search_form'] = search_form
        return context


class SearchView(TemplateView):
    template_name = 'search.html'

    def _search_talks(self, q):
        vector = SearchVector('title', weight='A') + SearchVector('description', weight='B')
        query = SearchQuery(q)
        rank = SearchRank(vector, query)
        search_results = Talk.objects.annotate(rank=rank).order_by('-rank')
        return search_results

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)

        search_form = SearchForm(self.request.GET)
        if search_form.is_valid():
            q = search_form.cleaned_data['q']
            search_results = self._search_talks(q)
            context['search_query'] = q
            context['search_results'] = search_results
        context['search_form'] = search_form

        return context
