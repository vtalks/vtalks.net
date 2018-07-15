from django.apps import AppConfig


class PlaylistsConfig(AppConfig):
    name = 'playlists'

    def ready(self):
        import playlists.signals
