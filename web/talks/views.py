from django.views.generic import TemplateView

from .models import Talk
from .forms import SearchForm

# Create your views here.


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['search_form'] = SearchForm()
        return context


class SearchView(TemplateView):
    template_name = 'search.html'

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        context['search_form'] = SearchForm()
        q = self.request.GET['q']
        context['search_results'] = Talk.objects.filter(title__search=q)
        return context