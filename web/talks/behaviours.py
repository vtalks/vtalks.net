import math

from django.db import models

from django.utils import timezone


class Rankable(models.Model):
    wilsonscore_rank = models.FloatField('wilson score rank', default=0)
    hacker_hot = models.FloatField('hackernews hot rank', default=0)

    class Meta:
        abstract = True

    def get_wilson_score(self, ups, downs, z=1.96):
        """
        Wilson score interval sort
        (popularized by reddit's best comment system)
        http://www.evanmiller.org/how-not-to-sort-by-average-rating.html
        """
        if ups == 0:
            return 0
        n = ups + downs
        p = ups / n
        sqrtexpr = (p * (1 - p) + z * z / (4 * n)) / n
        res = (p + z * z / (2 * n) - z * math.sqrt(sqrtexpr)) / (1 + z * z / n)
        return res

    def get_reddit_hot(self):
        """
        Reddit's hot sort
        (popularized by reddit's news ranking)
        http://amix.dk/blog/post/19588
        Corrected for decay errors in post
        """

        return 0

    def get_hacker_hot(self, votes, published, gravity=1.8):
        """
        Hackernews' hot sort
        http://amix.dk/blog/post/19574
        """
        gravity = 1.1

        try:
            d = timezone.now() - published
        except TypeError:
            return 0
        hour_age = d.total_seconds() // 3600
        res = votes / math.pow(hour_age + 2, gravity)
        return res
