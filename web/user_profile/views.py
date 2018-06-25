import json
import oauth2 as oauth

from urllib.parse import parse_qsl

from django.conf import settings
from django.views.generic import UpdateView
from django.views.generic import RedirectView
from django.contrib.auth import login
from django.contrib.auth.models import User

from .models import UserProfile

from .forms import AuthUserSettingsForm
from .forms import AuthProfileSettingsForm

# Create your views here.


class AuthTwitterView(RedirectView):
    url = "{:s}?oauth_token={:s}"

    def __get_oauth_client(self):
        consumer = oauth.Consumer(settings.TWITTER_TOKEN,
                                  settings.TWITTER_SECRET)
        oauth_client = oauth.Client(consumer)
        return oauth_client

    def __get_oauth_token(self):
        c = self.__get_oauth_client()
        resp, content = c.request(settings.TWITTER_REQUEST_TOKEN_URL, "GET")
        if resp['status'] != '200':
            raise Exception("Invalid response from Twitter.")
        data = dict(parse_qsl(content.decode('UTF-8')))
        s = self.request.session
        s['oauth_token'] = data['oauth_token']
        s['oauth_token_secret'] = data['oauth_token_secret']

    def get_redirect_url(self, *args, **kwargs):
        self.__get_oauth_token()
        self.url = self.url.format(settings.TWITTER_AUTHENTICATE_URL,
                                   self.request.session['oauth_token'])
        return super().get_redirect_url(*args, **kwargs)


class AuthTwitterCallbackView(RedirectView):
    pattern_name = 'home:index'

    def __get_oauth_client(self):
        consumer = oauth.Consumer(settings.TWITTER_TOKEN,
                                  settings.TWITTER_SECRET)
        oauth_token = self.request.session['oauth_token']
        oauth_token_secret = self.request.session['oauth_token_secret']
        token = oauth.Token(oauth_token, oauth_token_secret)
        token.set_verifier(self.request.GET['oauth_verifier'])
        oauth_client = oauth.Client(consumer, token)
        return oauth_client

    def __get_oauth_access_token(self):
        c = self.__get_oauth_client()
        resp, content = c.request(settings.TWITTER_ACCESS_TOKEN_URL, "POST")
        if resp['status'] != '200':
            raise Exception("Invalid response from Twitter.")
        data = dict(parse_qsl(content.decode('UTF-8')))
        s = self.request.session
        s['oauth_token'] = data['oauth_token']
        s['oauth_token_secret'] = data['oauth_token_secret']

    def __verify_credentials(self):
        c = self.__get_oauth_client()
        resp, content = c.request(settings.TWITTER_VERIFY_CREDENTIALS_URL, "GET")
        if resp['status'] != '200':
            raise Exception("Invalid response from Twitter.")
        return json.loads(content)

    def get_redirect_url(self, *args, **kwargs):
        self.__get_oauth_access_token()
        twitter_user = self.__verify_credentials()
        # Create or update user
        user_obj, created = User.objects.update_or_create(
            username=twitter_user["screen_name"],
            defaults={
                'username': twitter_user["screen_name"],
                'email': twitter_user["email"],
            },
        )
        # Update user profile
        profile = user_obj.profile
        profile.twitter_id = twitter_user["id"]
        profile.bio = twitter_user["description"]
        profile.avatar = twitter_user["profile_image_url"]
        profile.oauth_token = self.request.session["oauth_token"]
        profile.oauth_token_secret = self.request.session["oauth_token_secret"]
        profile.save()
        # Login user
        login(self.request, user_obj)
        return super().get_redirect_url(*args, **kwargs)


class AuthProfileSettingsView(UpdateView):
    template_name = 'settings.html'
    form_class = AuthUserSettingsForm
    success_url = '/auth/settings'

    def get_object(self, queryset=None):
        obj = User.objects.get(id=self.request.user.id)
        return obj

    def get_context_data(self, **kwargs):
        context = super(AuthProfileSettingsView, self).get_context_data(**kwargs)
        profile_obj = UserProfile.objects.get(user__id=self.request.user.id)
        context['profile_form'] = AuthProfileSettingsForm(instance=profile_obj)
        context['watched_talks'] = self.request.user.talkwatch_set.filter()
        context['liked_talks'] = self.request.user.talklike_set.filter()
        context['disliked_talks'] = self.request.user.talkdislike_set.filter()
        context['favorited_talks'] = self.request.user.talkfavorite_set.filter()
        return context
