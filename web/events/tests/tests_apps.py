from django.apps import apps
from django.test import TestCase

from events.apps import EventsConfig

# Create your tests here.


class EventsConfigTest(TestCase):
    def test_apps(self):
        self.assertEqual(EventsConfig.name, 'events')
        self.assertEqual(apps.get_app_config('events').name, 'events')
