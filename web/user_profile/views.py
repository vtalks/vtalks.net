import oauth2 as oauth

from urllib.parse import parse_qsl

from django.conf import settings
from django.http import HttpResponseRedirect
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth import logout
from django.contrib.auth import login
from django.contrib.auth.models import User

# TODO:
# - It's probably a good idea to put your consumer's OAuth token and OAuth secret into your project's settings.
consumer = oauth.Consumer(settings.TWITTER_TOKEN, settings.TWITTER_SECRET)
client = oauth.Client(consumer)

# Create your views here.


# TODO:
# - Port to RedirectView instead of View
class LogoutView(View):

    def get(self, request):
        # FIXME: Clean should not be necessary
        # Clean session
        if "oauth_token" in request.session:
            del request.session['oauth_token']
        if "oauth_token_secret" in request.session:
            del request.session['oauth_token_secret']
        if "user_id" in request.session:
            del request.session['user_id']
        if "user_name" in request.session:
            del request.session['user_name']
        if "twitter_id" in request.session:
            del request.session['twitter_id']
        # Logout user
        logout(request)
        return HttpResponseRedirect("/")


class LoginView(TemplateView):
    template_name = "login.html"


# TODO:
# - Port to RedirectView instead of View
class AuthTwitterView(View):
    
    def get(self, request):
        request_token_url = 'https://api.twitter.com/oauth/request_token'
        authenticate_url = 'https://api.twitter.com/oauth/authenticate'

        # Step 1. Get a request token from Twitter.
        resp, content = client.request(request_token_url, "GET")
        if resp['status'] != '200':
            raise Exception("Invalid response from Twitter.")
        
        # Step 2. Store the request token in a session for later use.
        data = dict(parse_qsl(content))
        request.session['oauth_token'] = data[b'oauth_token'].decode('UTF-8')
        request.session['oauth_token_secret'] = data[b'oauth_token_secret'].decode('UTF-8')

        # Step 3. Redirect the user to the authentication URL.
        url = "%s?oauth_token=%s" % (authenticate_url, request.session['oauth_token'])
        return HttpResponseRedirect(url)


# TODO:
# - Port to RedirectView instead of View
class AuthTwitterCallbackView(View):

    def get(self, request):
        access_token_url = 'https://api.twitter.com/oauth/access_token'

        # Step 1. Use the request token in the session to build a new client.
        token = oauth.Token(request.session['oauth_token'], request.session['oauth_token_secret'])
        token.set_verifier(request.GET['oauth_verifier'])
        oath_client = oauth.Client(consumer, token)

        # Step 2. Request the authorized access token from Twitter.
        resp, content = oath_client.request(access_token_url, "GET")
        if resp['status'] != '200':
            raise Exception("Invalid response from Twitter.")

        data = dict(parse_qsl(content))
        twitter_id = data[b'user_id'].decode('UTF-8')
        screen_name = data[b'screen_name'].decode('UTF-8')

        # FIXME:
        # - Update last-login field
        #
        # TODO:
        # - Add support for email
        user_obj, created = User.objects.update_or_create(
            username=screen_name,
            defaults={
                'username': screen_name,
            },
        )
        user_obj.profile.twitter_id = twitter_id
        user_obj.profile.oauth_token = request.session['oauth_token']
        user_obj.profile.oauth_token_secret = request.session['oauth_token_secret']
        # TODO:
        # - Add support for bio
        # - Add support for avatar
        user_obj.save()

        # FIXME: This is probably not necessary
        request.session['user_id'] = user_obj.id
        request.session['user_username'] = user_obj.username
        request.session['twitter_id'] = twitter_id

        # Login user
        login(request, user_obj)

        return HttpResponseRedirect("/")
