from django.apps import apps
from django.test import TestCase
from ..apps import PlaylistsConfig

# Create your tests here.


class PlaylistsConfigTest(TestCase):
    def test_apps(self):
        self.assertEqual(PlaylistsConfig.name, 'playlists')
        self.assertEqual(apps.get_app_config('playlists').name, 'playlists')
