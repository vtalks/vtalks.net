from datetime import timedelta

from django.test import TestCase

from .timedelta import timedelta_nozeros

# Create your tests here.


class TimedeltaTests(TestCase):

    def test_dummy(self):
        pass

    def test_timedelta_nozeros_none_argument(self):
        expected_result = ''
        result = timedelta_nozeros(None)
        self.assertEquals(result, expected_result)

    def test_timedelta_nozeros_minute_seconds(self):
        d = timedelta(seconds=65)
        expected_results = '01:05'
        result = timedelta_nozeros(d)
        self.assertEquals(result, expected_results)

    def test_timedelta_nozeros_minutes_seconds(self):
        d = timedelta(seconds=809)
        expected_results = '13:29'
        result = timedelta_nozeros(d)
        self.assertEquals(result, expected_results)

    def test_timedelta_nozeros_hour_minutes_seconds(self):
        d = timedelta(seconds=5089)
        expected_results = '01:24:49'
        result = timedelta_nozeros(d)
        self.assertEquals(result, expected_results)

    def test_timedelta_nozeros_hours_minutes_seconds(self):
        d = timedelta(seconds=82089)
        expected_results = '22:48:09'
        result = timedelta_nozeros(d)
        self.assertEquals(result, expected_results)
