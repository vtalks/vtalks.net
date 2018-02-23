from django.apps import apps
from django.test import TestCase
from ..apps import TalksConfig

# Create your tests here.


class TalksConfigTest(TestCase):
    def test_apps(self):
        self.assertEqual(TalksConfig.name, 'talks')
        self.assertEqual(apps.get_app_config('talks').name, 'talks')
