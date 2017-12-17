from django.views.generic import View
from django.shortcuts import render

# Create your views here.

class IndexView(View):
    context = {}
    template = 'index.html'

    def get(self, request):
        print(request.user)
        return render(request, self.template, self.context)
