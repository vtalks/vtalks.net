from django.test import TestCase

from django.contrib.auth.models import User

from .models import UserProfile

# Create your tests here.


class UserProfileModelTests(TestCase):

    def setUp(self):
        User.objects.create_user('user_1', password='userpass')

    def test_instance_get_string_repr(self):
        user_profile_1 = UserProfile.objects.get(user__username='user_1')
        self.assertEquals(str(user_profile_1), 'user_1')
