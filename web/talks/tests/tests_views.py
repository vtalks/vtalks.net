from django.test import TestCase
from django.test import Client

from channels.models import Channel
from talks.models import Talk

# Create your tests here.


class TalksViewsTest(TestCase):

    def setUp(self):
        chanel_1 = Channel.objects.create(code='1', title='channel title 1')
        Talk.objects.create(code='1', title='talk title 1', channel=chanel_1)
        Talk.objects.create(code='2', title='talk title 2', channel=chanel_1)
        Talk.objects.create(code='3', title='talk title 3', channel=chanel_1)
        Talk.objects.create(code='4', title='talk title 4', channel=chanel_1)
        # Every test needs a client.
        self.client = Client()

    def test_home_http_200(self):
        # Issue a GET request.
        response = self.client.get('/')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_details_talk_http_200(self):
        # Issue a GET request.
        response = self.client.get('/talk/talk-title-1/')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_latest_talks_http_200(self):
        # Issue a GET request.
        response = self.client.get('/latest')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_best_talks_http_200(self):
        # Issue a GET request.
        response = self.client.get('/best')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
