from django.test import TestCase

from .models import Channel
from .models import Talk

# Create your tests here.


class ChannelModelTests(TestCase):

    def test_dummy(self):
        """Dummy Test"""
        pass

    def test_instance_to_string(self):
        """The string representation of a Channel model is its own title"""
        channel = Channel(code='1234', title='channel title')
        self.assertEquals(str(channel), 'channel title')

    def test_instance_get_youtube_valid_url(self):
        """All Channel models have a property that returns the external youtube url"""
        channel = Channel(code='1234', title='channel title')
        self.assertEquals(channel.youtube_url, 'https://www.youtube.com/channel/1234')

    def test_instance_get_youtube_null_url(self):
        """All Channel models have a property that returns the external youtube url
        If the code is not set the youtube url will be '-'."""
        channel = Channel(title='channel title')
        self.assertEquals(channel.youtube_url, '-')


class TalkModelTests(TestCase):

    def test_dummy(self):
        """Dummy Test"""
        pass

    def test_instance_to_string(self):
        """The string representation of a Talk model is its own title"""
        talk = Talk(code='1234', title='talk title')
        self.assertEquals(str(talk), 'talk title')

    def test_instance_get_youtube_valid_url(self):
        """All Talk models have a property that returns the external youtube url"""
        talk = Talk(code='1234', title='talk title')
        self.assertEquals(talk.youtube_url, 'https://www.youtube.com/watch?v=1234')

    def test_instance_get_youtube_null_url(self):
        """All Talk models have a property that returns the external youtube url
        If the code is not set the youtube url will be '-'."""
        talk = Talk(title='talk title')
        self.assertEquals(talk.youtube_url, '-')

    def test_instance_thumbnails(self):
        """A talk have a set of thumbnails of different resolutions based on its code"""
        talk = Talk(code='1234', title='talk title')
        self.assertEquals(talk.default_thumb, 'https://i.ytimg.com/vi/1234/default.jpg')
        self.assertEquals(talk.medium_thumb, 'https://i.ytimg.com/vi/1234/mqdefault.jpg')
        self.assertEquals(talk.high_thumb, 'https://i.ytimg.com/vi/1234/hqdefault.jpg')
        self.assertEquals(talk.standard_thumb, 'https://i.ytimg.com/vi/1234/sddefault.jpg')
        self.assertEquals(talk.maxres_thumb, 'https://i.ytimg.com/vi/1234/maxresdefault.jpg')

    def test_instance_null_thumbnails(self):
        """A talk have a set of thumbnails of different resolutions based on its code
        If the code is not set the youtube url will be '-'."""
        talk = Talk(title='talk title')
        self.assertEquals(talk.default_thumb, '-')
        self.assertEquals(talk.medium_thumb, '-')
        self.assertEquals(talk.high_thumb, '-')
        self.assertEquals(talk.standard_thumb, '-')
        self.assertEquals(talk.maxres_thumb, '-')

    def test_instance_slug(self):
        """A talk populates automatically an slug field once it is created"""
        channel = Channel(code='1234', title='channel title')
        channel.save()
        talk = Talk(code='1234', title='talk title', channel_id='1')
        talk.save()
        self.assertEquals(talk.slug, 'talk-title')

    def test_duplicate_title_slug(self):
        """It is possible than two different talks have the same title, in this case
        the slug will have the talk code as a suffix on the second talk."""
        talk_a = Talk(code='1234', title='talk title', channel_id='1')
        talk_a.save()
        talk_b = Talk(code='4321', title='talk title', channel_id='1')
        talk_b.save()
        self.assertEquals(talk_b.slug, 'talk-title-4321')
