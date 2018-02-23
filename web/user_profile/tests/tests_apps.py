from django.apps import apps
from django.test import TestCase
from ..apps import UserProfileConfig

# Create your tests here.


class UserProfileConfigTest(TestCase):
    def test_apps(self):
        self.assertEqual(UserProfileConfig.name, 'user_profile')
        self.assertEqual(apps.get_app_config('user_profile').name, 'user_profile')
