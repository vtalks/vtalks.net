from django.test import TestCase
from django.utils import timezone

from .popularity import reddit_hot
from .popularity import wilson_score
from .popularity import hacker_hot

# Create your tests here.


class DecayPopularityTests(TestCase):

    def test_dummy(self):
        pass

    def test_reddit_hot(self):
        res = reddit_hot()
        self.assertEquals(res, 0)

    def test_wilson_score(self):
        ups = 10
        downs = 3
        res = wilson_score(ups, downs)
        self.assertEquals(res, 0.49743126004873084)

    def test_wilson_score_ups_0(self):
        ups = 0
        downs = 3
        res = wilson_score(ups, downs)
        self.assertEquals(res, 0)

    def test_hacker_hot(self):
        votes = 359478
        published = timezone.now()
        res = hacker_hot(votes, published)
        self.assertGreater(res, 0)
