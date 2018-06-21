from django.test import TestCase

from playlists.models import Playlist

# Create your tests here.


class PlaylistModelTests(TestCase):

    def setUp(self):
        Playlist.objects.create(code='1', title='playlist title 1')

    def test_instance_get_string_repr(self):
        """ Playlist object string representation returns its title
        """
        playlist_1 = Playlist.objects.get(code='1')
        self.assertEquals(str(playlist_1), playlist_1.title)

    def test_instance_get_youtube_valid_url(self):
        """ All Playlist models have a property that returns the external
        youtube url.
        """
        playlist_1 = Playlist.objects.get(code='1')
        self.assertEquals(playlist_1.youtube_url, 'https://www.youtube.com/playlist?list=1')