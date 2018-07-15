import math


from django.views.generic.list import ListView
from django.conf import settings

from .forms import SearchForm

from talks.models import Talk
from search.search import search_talks


class SearchTalksView(ListView):
    model = Talk
    template_name = 'search.html'
    paginate_by = settings.PAGE_SIZE

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

            results_total, results_ids = search_talks(q=query, page=page, sort=sort)
            search_results = Talk.published_objects.filter(pk__in=results_ids)

            num_pages = math.ceil(results_total / self.paginate_by)
            if num_pages > 500:
                num_pages = 500
            pagination = {
                "is_paginated": True if results_total > self.paginate_by else False,
                "number": page,
                "num_pages": num_pages,
                "has_previous": True if page > 1 else False,
                "previous_page_number": page - 1,
                "has_next": True if page < num_pages else False,
                "next_page_number": page + 1,
            }
            context['pagination'] = pagination
            context['sort'] = sort
            context['object_list'] = search_results

        return context
