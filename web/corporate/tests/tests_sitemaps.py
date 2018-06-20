from django.test import TestCase

from channels.models import Channel
from talks.models import Talk

# Create your tests here.


class SitemapTest(TestCase):

    def setUp(self):
        chanel_1 = Channel.objects.create(code='1', title='channel title 1')
        Talk.objects.create(code='1', title='talk title 1', channel=chanel_1)
        Talk.objects.create(code='11', title='talk title same title', channel=chanel_1)
        Talk.objects.create(code='12', title='talk title same title', channel=chanel_1)

    def test_sitemap(self):
        # Get sitemap
        response = self.client.get('/sitemap.xml')

        # Check post is present in sitemap

        self.assertTrue("talk-title-1" in str(response.content))

        # Check about page is present in sitemap
        self.assertTrue("/corporate/about" in str(response.content))

        # Check contact page is present in sitemap
        self.assertTrue("/corporate/contact" in str(response.content))
