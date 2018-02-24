from django.test import TestCase

from channels.models import Channel
from talks.models import Talk

# Create your tests here.


class ChannelModelTests(TestCase):

    def setUp(self):
        Channel.objects.create(code='1', title='channel title 1')

    def test_instance_get_string_repr(self):
        """Channel object string representation returns its title"""
        channel_1 = Channel.objects.get(code='1')
        self.assertEquals(str(channel_1), channel_1.title)

    def test_instance_get_youtube_valid_url(self):
        """All Channel models have a property that returns the external
        youtube url.
        """
        channel_1 = Channel.objects.get(code='1')
        self.assertEquals(channel_1.youtube_url, 'https://www.youtube.com/channel/1')


class TalkModelTests(TestCase):

    def setUp(self):
        chanel_1 = Channel.objects.create(code='1', title='channel title 1')
        Talk.objects.create(code='1', title='talk title 1', channel=chanel_1)
        Talk.objects.create(code='11', title='talk title same title', channel=chanel_1)
        Talk.objects.create(code='12', title='talk title same title', channel=chanel_1)

    def test_instance_get_string_repr(self):
        """Talk object string representation returns its title"""
        talk_1 = Talk.objects.get(code='1')
        self.assertEquals(str(talk_1), talk_1.title)

    def test_instance_get_youtube_valid_url(self):
        """All Talk models have a property that returns the external youtube
        url.
        """
        talk_1 = Talk.objects.get(code='1')
        self.assertEquals(talk_1.youtube_url,
                          'https://www.youtube.com/watch?v=1')

    def test_instance_thumbnails(self):
        """A talk have a set of thumbnails of different resolutions based on
        its code.
        """
        talk_1 = Talk.objects.get(code='1')
        self.assertEquals(talk_1.default_thumb,
                          'https://i.ytimg.com/vi/1/default.jpg')
        self.assertEquals(talk_1.medium_thumb,
                          'https://i.ytimg.com/vi/1/mqdefault.jpg')
        self.assertEquals(talk_1.high_thumb,
                          'https://i.ytimg.com/vi/1/hqdefault.jpg')
        self.assertEquals(talk_1.standard_thumb,
                          'https://i.ytimg.com/vi/1/sddefault.jpg')
        self.assertEquals(talk_1.maxres_thumb,
                          'https://i.ytimg.com/vi/1/maxresdefault.jpg')

    def test_create_talk_slug(self):
        """A talk populates automatically an slug field once it is created"""
        talk_1 = Talk.objects.get(code='1')
        self.assertEquals(talk_1.slug, 'talk-title-1')

    def test_create_duplicate_title_slug(self):
        """Test duplicate talk title

        It is possible than two different talks have the same title, in this
        case the slug will have the talk code as a suffix on the second talk.
        """
        talk_12 = Talk.objects.get(code='12')
        self.assertEquals(talk_12.slug, 'talk-title-same-title-12')

    def test_save_talk_slug(self):
        """Test save talk slug

        If the title on already created talk is changed, the slug of the talk
        is not modified when it is saved.
        """
        talk_1 = Talk.objects.get(code=1)
        talk_1.title = "another title"
        talk_1.save()
        self.assertEquals(talk_1.slug, 'talk-title-1')
