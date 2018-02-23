from django.apps import apps
from django.test import TestCase
from .apps import CorporateConfig

# Create your tests here.


class CorporateConfigTest(TestCase):
    def test_apps(self):
        self.assertEqual(CorporateConfig.name, 'corporate')
        self.assertEqual(apps.get_app_config('corporate').name, 'corporate')
