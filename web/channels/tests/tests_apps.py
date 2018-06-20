from django.apps import apps
from django.test import TestCase
from ..apps import ChannelsConfig

# Create your tests here.


class ChannelsConfigTest(TestCase):

    def test_apps(self):
        self.assertEqual(ChannelsConfig.name, 'channels')
        self.assertEqual(apps.get_app_config('channels').name, 'channels')
