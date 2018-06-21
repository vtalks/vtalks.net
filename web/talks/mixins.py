from django.db import models

from ranking_sorting import wilson_score
from ranking_sorting import hackernews_hot


class Rankable(models.Model):
    wilsonscore_rank = models.FloatField('wilson score rank', default=0)
    hacker_hot = models.FloatField('hackernews hot rank', default=0)

    class Meta:
        abstract = True

    def get_wilson_score(self, ups, downs, z=1.96):
        res = wilson_score.wilson_score(ups, downs, z)
        return res

    def get_hacker_hot(self, votes, published, gravity=1.8):
        res = hackernews_hot.hackernews_hot(votes, published, gravity)
        return res
