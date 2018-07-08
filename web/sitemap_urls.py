from django.urls import path
from django.contrib.sitemaps.views import sitemap

from talks.sitemaps import HomeSitemap
from talks.sitemaps import TalksSitemap
from corporate.sitemaps import StaticSitemap

sitemaps = {
    'home': HomeSitemap,
    'talks': TalksSitemap,
    'static': StaticSitemap,
}

urlpatterns = [
    path('', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]