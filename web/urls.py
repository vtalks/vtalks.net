"""vtalks.net URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.urls import include
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('user_profile.urls')),
    path('corporate/', include('corporate.urls')),
    path('topic/', include('topics.urls')),
    path('tag/', include('tags.urls')),
    path('search/', include('search.urls')),
    path('api/', include('api_urls')),
    path('channel/', include('channels.urls')),
    path('', include('talks.urls')),
    path('', include('home.urls')),

    path('sitemap.xml', include('sitemap_urls'))
]
