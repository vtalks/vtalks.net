from django.apps import AppConfig


class ChannelsConfig(AppConfig):
    name = 'channels'

    def ready(self):
        import channels.signals
