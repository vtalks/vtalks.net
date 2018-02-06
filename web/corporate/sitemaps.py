
from django.contrib import sitemaps
from django.urls import reverse

from talks.models import Talk


class StaticSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        return ['talks:index', 'corporate:about', 'corporate:contact', 'corporate:help', 'corporate:terms', 'corporate:privacy']

    def location(self, item):
        return reverse(item)


class TalksSitemap(sitemaps.Sitemap):
    priority = 0.8
    changefreq = 'daily'

    def items(self):
        return Talk.objects.all()

    def lastmod(self, item):
        return item.created
