from django.test import TestCase
from django.test import Client

# Create your tests here.


class CorporateViewsTest(TestCase):

    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_corporate_about_http_200(self):
        # Issue a GET request.
        response = self.client.get('/corporate/about')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_corporate_help_http_200(self):
        # Issue a GET request.
        response = self.client.get('/corporate/help')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_corporate_contact_http_200(self):
        # Issue a GET request.
        response = self.client.get('/corporate/contact')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
