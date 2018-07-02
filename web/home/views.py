from django.views.generic import TemplateView

from home.search import search_talks
from talks.models import Talk
from topics.models import Topic

from search.forms import SearchForm

# Create your views here.


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        search_form = SearchForm()
        context['search_form'] = search_form

        results_total, results_ids = search_talks(page=1, sort="created")
        latest_talks = Talk.published_objects.filter(pk__in=results_ids)[:3]
        context['latest_talks'] = latest_talks

        results_total, results_ids = search_talks(page=1, sort="wilsonscore_rank")
        best_talks = Talk.published_objects.filter(pk__in=results_ids)[:3]
        context['best_talks'] = best_talks

        context['topics'] = Topic.published_objects.all().order_by('?')[:5]

        return context
