from django.apps import AppConfig

# Application Configuration


class UserProfileConfig(AppConfig):
    name = 'user_profile'
    verbose_name = 'User Profile'

    def ready(self):
        """Override this to put in:
            Users system checks
            Users signal registration
        """
        pass