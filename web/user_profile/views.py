import oauth2 as oauth

from urllib.parse import parse_qsl

from django.conf import settings
from django.views.generic import TemplateView
from django.views.generic import RedirectView
from django.contrib.auth import logout
from django.contrib.auth import login
from django.contrib.auth.models import User

# Create your views here.


class LogoutView(RedirectView):
    pattern_name = 'index'

    def __logout_user(self):
        # Logout user & clear session.
        logout(self.request)

    def get_redirect_url(self, *args, **kwargs):
        self.__logout_user()
        return super().get_redirect_url(*args, **kwargs)


class LoginView(TemplateView):
    template_name = "login.html"


class AuthTwitterView(RedirectView):
    # The URL to redirect to, as a string. Or None to raise a 410 (Gone)
    # HTTP error.
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
        data = dict(parse_qsl(content))
        s = self.request.session
        s['oauth_token'] = data[b'oauth_token'].decode('UTF-8')
        s['oauth_token_secret'] = data[b'oauth_token_secret'].decode('UTF-8')
        return s['oauth_token'], s['oauth_token_secret']

    def get_redirect_url(self, *args, **kwargs):
        oauth_token, oauth_token_secret = self.__get_oauth_token()
        base_url = settings.TWITTER_AUTHENTICATE_URL
        self.url = self.url.format(base_url, oauth_token)
        return super().get_redirect_url(*args, **kwargs)


class AuthTwitterCallbackView(RedirectView):
    # The name of the URL pattern to redirect to. Reversing will be done using
    # the same args and kwargs as are passed in for this view
    pattern_name = 'index'

    def __get_oauth_client(self):
        consumer = oauth.Consumer(settings.TWITTER_TOKEN,
                                  settings.TWITTER_SECRET)
        s = self.request.session
        token = oauth.Token(s['oauth_token'], s['oauth_token_secret'])
        token.set_verifier(self.request.GET['oauth_verifier'])
        oauth_client = oauth.Client(consumer, token)
        return oauth_client

    def __get_oauth_access_token(self):
        c = self.__get_oauth_client()
        resp, content = c.request(settings.TWITTER_ACCESS_TOKEN_URL, "GET")
        if resp['status'] != '200':
            raise Exception("Invalid response from Twitter.")
        data = dict(parse_qsl(content))
        oauth_token = data[b'oauth_token'].decode('UTF-8')
        oauth_token_secret = data[b'oauth_token_secret'].decode('UTF-8')
        twitter_id = data[b'user_id'].decode('UTF-8')
        screen_name = data[b'screen_name'].decode('UTF-8')
        return oauth_token, oauth_token_secret, twitter_id, screen_name

    def __login_user(self, token, token_secret, twitter_id, screen_name):
        # FIXME:
        # - Update last-login field
        #
        # TODO:
        # - Add support for email
        user_obj, created = User.objects.update_or_create(
            username=screen_name,
            defaults={'username': screen_name, },
        )
        profile = user_obj.profile
        profile.twitter_id = twitter_id
        profile.oauth_token = token
        profile.oauth_token_secret = token_secret
        # TODO:
        # - Add support for bio
        # - Add support for avatar
        user_obj.save()
        # Login user
        login(self.request, user_obj)

    def get_redirect_url(self, *args, **kwargs):
        t, t_secret, u_id, u_login = self.__get_oauth_access_token()
        self.__login_user(t, t_secret, u_id, u_login)
        return super().get_redirect_url(*args, **kwargs)
