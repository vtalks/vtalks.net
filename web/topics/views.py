from django.views.generic.detail import DetailView
from django.core.paginator import Paginator
from django.conf import settings

from topics.models import Topic

from talks.forms import SearchForm


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

        topic_talks = topic.get_talks(count=None)
        paginator = Paginator(topic_talks, self.paginate_by)

        page = 1
        if "page" in self.kwargs:
            page = self.kwargs["page"]
        context['is_paginated'] = True
        context['object_list'] = paginator.get_page(page)

        return context
