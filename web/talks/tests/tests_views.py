from django.test import TestCase
from django.test import Client

# Create your tests here.


class TalksConfigTest(TestCase):

    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_home_http_200(self):
        # Issue a GET request.
        response = self.client.get('/')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        # Check that the rendered context contains 5 customers.
        # self.assertEqual(len(response.context['customers']), 5)
