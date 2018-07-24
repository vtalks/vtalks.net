import math

from django.views.generic import RedirectView
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.contrib.syndication.views import Feed
from django.utils import timezone
from django.utils.feedgenerator import Atom1Feed
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.http import Http404

from .search import search_talks
from .search import search_more_like_this
from .models import Talk
from .models import TalkLike
from .models import TalkDislike
from .models import TalkFavorite
from .models import TalkWatch

from search.forms import SearchForm

# Create your views here.


class DetailTalkView(DetailView):
    model = Talk
    template_name = 'details-talk.html'

    def get_object(self, queryset=None):
        obj = super(DetailTalkView, self).get_object(queryset=queryset)
        if not obj.published:
            raise Http404()
        return obj

    def get_context_data(self, **kwargs):
        context = super(DetailTalkView, self).get_context_data(**kwargs)

        # Views +1 (autoplay)
        talk = self.get_object()
        talk.view_count += 1

        # Update talk to the database
        talk.updated = timezone.now()
        talk.save()

        watched = None
        if self.request.user.is_authenticated:
            try:
                watched = TalkWatch.objects.get(user=self.request.user, talk=talk)
            except ObjectDoesNotExist:
                pass
        context['watched'] = watched

        favorited = None
        if self.request.user.is_authenticated:
            try:
                favorited = TalkFavorite.objects.get(user=self.request.user, talk=talk)
            except ObjectDoesNotExist:
                pass
        context['favorited'] = favorited

        liked = None
        if self.request.user.is_authenticated:
            try:
                liked = TalkLike.objects.get(user=self.request.user, talk=talk)
            except ObjectDoesNotExist:
                pass
        context['liked'] = liked

        disliked = None
        if self.request.user.is_authenticated:
            try:
                disliked = TalkDislike.objects.get(user=self.request.user, talk=talk)
            except ObjectDoesNotExist:
                pass
        context['disliked'] = disliked

        search_form = SearchForm()
        context['search_form'] = search_form

        results_total, results_ids = search_talks(page=1, sort="hacker_hot")
        hot_talks = Talk.published_objects.filter(pk__in=results_ids)[:4]
        context['hot_talks'] = hot_talks

        results_total, results_ids = search_more_like_this(talk)
        context['related_talks'] = Talk.published_objects.filter(pk__in=results_ids)

        return context


class LatestTalksView(TemplateView):
    template_name = 'latest-talks.html'
    paginate_by = settings.PAGE_SIZE

    def get_context_data(self, **kwargs):
        context = super(LatestTalksView, self).get_context_data(**kwargs)

        search_form = SearchForm()
        context['search_form'] = search_form

        page = 1
        if "page" in self.kwargs:
            page = int(self.kwargs["page"])

        sort = "created"

        results_total, results_ids = search_talks(page=page, sort=sort)
        search_results = Talk.published_objects.filter(pk__in=results_ids)

        num_pages = math.ceil(results_total / self.paginate_by)
        if num_pages > 500:
            num_pages = 500
        pagination = {
            "is_paginated": True if results_total > self.paginate_by else False,
            "number": page,
            "num_pages": num_pages,
            "has_previous": True if page > 1 else False,
            "previous_page_number": page - 1,
            "has_next": True if page < num_pages else False,
            "next_page_number": page + 1,
        }
        context['pagination'] = pagination
        context['object_list'] = search_results

        return context


class BestTalksView(TemplateView):
    template_name = 'best-talks.html'
    paginate_by = settings.PAGE_SIZE

    def get_context_data(self, **kwargs):
        context = super(BestTalksView, self).get_context_data(**kwargs)

        search_form = SearchForm()
        context['search_form'] = search_form

        page = 1
        if "page" in self.kwargs:
            page = int(self.kwargs["page"])

        sort = "wilsonscore_rank"

        results_total, results_ids = search_talks(page=page, sort=sort)
        search_results = Talk.published_objects.filter(pk__in=results_ids)

        num_pages = math.ceil(results_total / self.paginate_by)
        if num_pages > 500:
            num_pages = 500
        pagination = {
            "is_paginated": True if results_total > self.paginate_by else False,
            "number": page,
            "num_pages": num_pages,
            "has_previous": True if page > 1 else False,
            "previous_page_number": page - 1,
            "has_next": True if page < num_pages else False,
            "next_page_number": page + 1,
        }
        context['pagination'] = pagination
        context['object_list'] = search_results

        return context


class LikeTalkView(RedirectView):
    permanent = False
    pattern_name = 'talks:talk-details'

    def get_redirect_url(self, *args, **kwargs):
        slug = self.kwargs['slug']
        talk = Talk.published_objects.get(slug=slug)

        if self.request.user.is_authenticated:
            liked = TalkLike.objects.filter(user=self.request.user, talk=talk)
            if not liked:
                # delete talk disliked
                TalkDislike.objects.filter(user=self.request.user, talk=talk).delete()
                # create talk like
                TalkLike.objects.create(user=self.request.user, talk=talk)
                # update like count
                talk.like_count += 1
                talk.save()

        return super().get_redirect_url(*args, **kwargs)


class DislikeTalkView(RedirectView):
    permanent = False
    pattern_name = 'talks:talk-details'

    def get_redirect_url(self, *args, **kwargs):
        slug = self.kwargs['slug']
        talk = Talk.published_objects.get(slug=slug)

        if self.request.user.is_authenticated:
            disliked = TalkDislike.objects.filter(user=self.request.user, talk=talk)
            if not disliked:
                # delete talk liked
                TalkLike.objects.filter(user=self.request.user, talk=talk).delete()
                # create talk dislike
                TalkDislike.objects.create(user=self.request.user, talk=talk)
                # update dislike count
                talk.dislike_count += 1
                talk.save()

        return super().get_redirect_url(*args, **kwargs)


class FavoriteTalkView(RedirectView):
    permanent = False
    pattern_name = 'talks:talk-details'

    def get_redirect_url(self, *args, **kwargs):
        slug = self.kwargs['slug']
        talk = Talk.published_objects.get(slug=slug)

        if self.request.user.is_authenticated:
            favorited = TalkFavorite.objects.filter(user=self.request.user, talk=talk)
            if not favorited:
                # create talk like
                TalkFavorite.objects.create(user=self.request.user, talk=talk)
                # update favorite count
                talk.favorite_count += 1
                talk.save()

        return super().get_redirect_url(*args, **kwargs)


class WatchTalkView(RedirectView):
    permanent = False
    pattern_name = 'talks:talk-details'

    def get_redirect_url(self, *args, **kwargs):
        slug = self.kwargs['slug']
        talk = Talk.published_objects.get(slug=slug)

        if self.request.user.is_authenticated:
            watched = TalkWatch.objects.filter(user=self.request.user, talk=talk)
            if not watched:
                # create talk like
                TalkWatch.objects.create(user=self.request.user, talk=talk)
                talk.save()

        return super().get_redirect_url(*args, **kwargs)


class RSSLatestView(Feed):
    feed_type = Atom1Feed
    title = "Latest talks"
    link = "/latest/"
    description = "Latest published talks on vtalks.net."
    description_template = "feeds/latest.html"

    def items(self):
        return Talk.published_objects.order_by('-created')[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

    def item_updateddate(self, item):
        return item.updated

    def item_pubdate(self, item):
        return item.created

    # item_link is only needed if NewsItem has no get_absolute_url method.
    def item_link(self, item):
        return reverse('talks:talk-details', kwargs={'slug': item.slug})