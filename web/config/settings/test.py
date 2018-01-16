from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'web/db.sqlite3'),
    }
}

# Twitter configuration

TWITTER_AUTHENTICATE_URL = 'https://api.twitter.com/oauth/authenticate'
TWITTER_REQUEST_TOKEN_URL = 'https://api.twitter.com/oauth/request_token'
TWITTER_ACCESS_TOKEN_URL = 'https://api.twitter.com/oauth/access_token'
# https://developer.twitter.com/en/docs/accounts-and-users/manage-account-settings/api-reference/get-account-verify_credentials
TWITTER_VERIFY_CREDENTIALS_URL = 'https://api.twitter.com/1.1/account/verify_credentials.json?include_entities=false&skip_status=true&include_email=true'
TWITTER_TOKEN = os.getenv('TWITTER_TOKEN')
TWITTER_SECRET = os.getenv('TWITTER_SECRET')

# Youtube configuration

YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
