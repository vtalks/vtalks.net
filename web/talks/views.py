from django.views.generic import TemplateView

from django.contrib.postgres.search import SearchVector
from django.contrib.postgres.search import SearchQuery
from django.contrib.postgres.search import SearchRank
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from django.conf import settings
from django.core.paginator import Paginator

from .models import Talk

from taggit.models import Tag

from .forms import SearchForm

# Create your views here.


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        search_form = SearchForm()
        context['search_form'] = search_form

        latest_talks = Talk.objects.all().order_by('-created', '-youtube_view_count', '-youtube_like_count', 'youtube_dislike_count', '-updated')[:3]
        context['latest_talks'] = latest_talks

        best_talks = Talk.objects.all().order_by('-wilsonscore_rank', '-youtube_view_count', '-youtube_like_count', 'youtube_dislike_count', '-created', '-updated')[:3]
        context['best_talks'] = best_talks

        return context


class DetailTalkView(DetailView):
    model = Talk
    template_name = 'details-talk.html'

    def get_context_data(self, **kwargs):
        context = super(DetailTalkView, self).get_context_data(**kwargs)

        search_form = SearchForm()
        context['search_form'] = search_form

        return context


class LatestTalksView(ListView):
    model = Talk
    template_name = 'latest-talks.html'
    paginate_by = settings.PAGE_SIZE
    ordering = ['-created', '-youtube_view_count', '-youtube_like_count', 'youtube_dislike_count', '-updated']

    def get_context_data(self, **kwargs):
        context = super(LatestTalksView, self).get_context_data(**kwargs)

        search_form = SearchForm()
        context['search_form'] = search_form

        return context


class BestTalksView(ListView):
    model = Talk
    template_name = 'best-talks.html'
    paginate_by = settings.PAGE_SIZE
    ordering = ['-wilsonscore_rank', '-youtube_view_count', '-youtube_like_count', 'youtube_dislike_count', '-created', '-updated']

    def get_context_data(self, **kwargs):
        context = super(BestTalksView, self).get_context_data(**kwargs)

        search_form = SearchForm()
        context['search_form'] = search_form

        return context


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


class DetailTagView(DetailView):
    model = Tag
    template_name = 'details-tag.html'
    paginate_by = settings.PAGE_SIZE

    def get_context_data(self, **kwargs):
        context = super(DetailTagView, self).get_context_data(**kwargs)

        search_form = SearchForm()
        context['search_form'] = search_form

        slug = self.kwargs['slug']
        context['object'] = Tag.objects.get(slug=slug)

        tagged_talks = Talk.objects.filter(tags__slug__in=[slug]).order_by('-wilsonscore_rank', '-youtube_view_count', '-youtube_like_count', 'youtube_dislike_count', '-created', '-updated')
        paginator = Paginator(tagged_talks, self.paginate_by)

        page = 1
        if "page" in self.kwargs:
            page = self.kwargs["page"]
        context['is_paginated'] = True
        context['object_list'] = paginator.get_page(page)

        return context
