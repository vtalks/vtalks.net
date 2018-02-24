from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from talks.models import Talk
from channels.models import Channel


class RandomTalkAPIViewTestCase(APITestCase):
    url = reverse("talks:random-talk")

    def setUp(self):
        chanel_1 = Channel.objects.create(code='1', title='channel title 1')
        Talk.objects.create(code='1', title='talk title 1', channel=chanel_1)
        Talk.objects.create(code='11', title='talk title same title', channel=chanel_1)
        Talk.objects.create(code='12', title='talk title same title', channel=chanel_1)

    def test_random_talk(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)