import math

from django.utils import timezone


def wilson_score(ups, downs, z=1.96):
    """
    Wilson score interval sort
    (popularized by reddit's best comment system)
    http://www.evanmiller.org/how-not-to-sort-by-average-rating.html
    """
    if ups == 0:
        return 0
    n = ups + downs
    p = ups/n
    sqrtexpr = (p * (1 - p) + z * z / (4 * n)) / n
    res = (p + z*z/(2*n) - z*math.sqrt(sqrtexpr)) / (1+z*z/n)
    return res


def reddit_hot():
    """
    Reddit's hot sort
    (popularized by reddit's news ranking)
    http://amix.dk/blog/post/19588
    Corrected for decay errors in post
    """

    return 0


def hacker_hot(votes, published, gravity=1.8):
    """
    Hackernews' hot sort
    http://amix.dk/blog/post/19574
    """
    d = timezone.now() - published
    hour_age = d.total_seconds()//3600
    res = (votes - 1) / math.pow(hour_age + 2, gravity)
    return res
