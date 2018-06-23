from django.contrib import sitemaps
from django.urls import reverse

from .models import Talk


class HomeSitemap(sitemaps.Sitemap):
    protocol = 'https'
    priority = 0.6
    changefreq = 'daily'

    def items(self):
        return ['home:index']

    def location(self, item):
        return reverse(item)


class TalksSitemap(sitemaps.Sitemap):
    protocol = 'https'
    priority = 0.7
    changefreq = 'daily'

    def items(self):
        return Talk.objects.all()

    def lastmod(self, item):
        return item.created