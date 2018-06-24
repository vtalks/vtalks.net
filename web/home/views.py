from django.views.generic import TemplateView

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

        latest_talks = Talk.published_objects.all()[:3]
        context['latest_talks'] = latest_talks

        best_talks = Talk.published_objects.all().order_by('-wilsonscore_rank', '-created')[:3]
        context['best_talks'] = best_talks

        context['topics'] = Topic.objects.all().order_by('?')[:5]

        return context