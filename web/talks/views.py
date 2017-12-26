from django.views.generic import TemplateView

from django.contrib.postgres.search import SearchVector
from django.contrib.postgres.search import SearchQuery
from django.contrib.postgres.search import SearchRank
from django.views.generic.list import ListView

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

        popular_talks = Talk.objects.all().order_by('-view_count', '-like_count', 'dislike_count', '-created', '-updated')[:3]
        context['popular_talks'] = popular_talks

        return context


class LatestTalksView(ListView):
    model = Talk
    template_name = 'latest-talks.html'
    paginate_by = settings.PAGE_SIZE


class PopularTalksView(ListView):
    model = Talk
    template_name = 'popular-talks.html'
    paginate_by = settings.PAGE_SIZE
    ordering = ['-view_count', '-like_count', 'dislike_count', '-created', '-updated']


class SearchTalksView(ListView):
    model = Talk
    template_name = 'search.html'
    paginate_by = settings.PAGE_SIZE

    def _search_talks(self, q):
        vector = SearchVector('title', weight='A') + SearchVector('description', weight='B')
        query = SearchQuery(q)
        rank = SearchRank(vector, query)
        search_results = Talk.objects.annotate(rank=rank)
        # Filter by minimum rank
        search_results = search_results.filter(rank__gte=0.1)
        # Sort by rank (descendant)
        search_results = search_results.order_by('-rank')
        return search_results

    def get_context_data(self, **kwargs):
        context = super(SearchTalksView, self).get_context_data(**kwargs)

        search_form = SearchForm(self.request.GET)
        context['search_form'] = search_form

        if search_form.is_valid():
            q = search_form.cleaned_data['q']
            context['search_query'] = q

            search_results = self._search_talks(q)
            paginator = Paginator(search_results, self.paginate_by)

            page = 1
            if "page" in self.request.GET:
                page = self.request.GET["page"]
            context['object_list'] = paginator.get_page(page)

        return context
