from django.apps import apps
from django.test import TestCase
from ..apps import TopicsConfig

# Create your tests here.


class ChannelsConfigTest(TestCase):

    def test_apps(self):
        self.assertEqual(TopicsConfig.name, 'topics')
        self.assertEqual(apps.get_app_config('topics').name, 'topics')
