from django.test import TestCase

from topics.models import Topic

# Create your tests here.


class TopicModelTests(TestCase):

    def setUp(self):
        Topic.objects.create(id=1, title='topic title 1', slug='topic-title-1')

    def test_instance_get_string_repr(self):
        """ Topic object string representation returns its title
        """
        topic_1 = Topic.objects.get(id='1')
        self.assertEquals(str(topic_1), topic_1.title)