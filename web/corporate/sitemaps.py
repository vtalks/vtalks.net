from django.contrib import sitemaps
from django.urls import reverse


class StaticSitemap(sitemaps.Sitemap):
    protocol = 'https'
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        return ['corporate:about', 'corporate:contact', 'corporate:help', 'corporate:terms', 'corporate:privacy']

    def location(self, item):
        return reverse(item)

