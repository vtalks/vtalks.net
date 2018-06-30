import math

from django.views.generic.detail import DetailView
from django.conf import settings

from topics.models import Topic
from topics.search import search_talks_by_topic
from talks.models import Talk
from search.forms import SearchForm

# Create your views here.


class DetailTopicView(DetailView):
    model = Topic
    template_name = 'details-topic.html'
    paginate_by = settings.PAGE_SIZE

    def get_context_data(self, **kwargs):
        context = super(DetailTopicView, self).get_context_data(**kwargs)

        search_form = SearchForm()
        context['search_form'] = search_form

        slug = self.kwargs['slug']
        topic = Topic.objects.get(slug=slug)
        context['object'] = topic

        page = 1
        if "page" in self.kwargs:
            page = self.kwargs["page"]

        sort = "relevance"
        if "sort" in self.request.GET:
            sort = self.request.GET["sort"]

        results_total, results_ids = search_talks_by_topic(topic, page=page, sort=sort)
        search_results = Talk.published_objects.filter(pk__in=results_ids)

        num_pages = math.ceil(results_total / self.paginate_by)
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
