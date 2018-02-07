from django.apps import AppConfig


class CorporateConfig(AppConfig):
    name = 'corporate'
    verbose_name = 'Corporate'

    def ready(self):
        """Override this to put in:
            Users system checks
            Users signal registration
        """
        pass
