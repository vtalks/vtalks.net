from django.test import TestCase
from django.utils import timezone

from channels.models import Channel
from talks.models import Talk

# Create your tests here.


class BehavioursRankableTests(TestCase):

    def setUp(self):
        chanel_1 = Channel.objects.create(code='1', title='channel title 1')
        Talk.objects.create(code='1', title='talk title 1', channel=chanel_1)
        Talk.objects.create(code='11', title='talk title same title', channel=chanel_1)
        Talk.objects.create(code='12', title='talk title same title', channel=chanel_1)

    def test_reddit_hot(self):
        talk_1 = Talk.objects.get(code='1')
        res = talk_1.get_reddit_hot()
        self.assertEquals(res, 0)

    def test_wilson_score(self):
        talk_1 = Talk.objects.get(code='1')
        ups = 10
        downs = 3
        res = talk_1.get_wilson_score(ups, downs)
        self.assertEquals(res, 0.49743126004873084)

    def test_wilson_score_ups_0(self):
        talk_1 = Talk.objects.get(code='1')
        ups = 0
        downs = 3
        res = talk_1.get_wilson_score(ups, downs)
        self.assertEquals(res, 0)

    def test_hacker_hot(self):
        talk_1 = Talk.objects.get(code='1')
        votes = 359478
        published = timezone.now()
        res = talk_1.get_hacker_hot(votes, published)
        self.assertGreater(res, 0)
