from django.apps import AppConfig

# Application Configuration


class TalksConfig(AppConfig):
    name = 'talks'

    def ready(self):
        import talks.signals
