from django.apps import AppConfig

# Application Configuration


class TalksConfig(AppConfig):
    name = 'talks'
    verbose_name = 'Talks'

    def ready(self):
        """Override this to put in:
            Users system checks
            Users signal registration
        """
        pass
