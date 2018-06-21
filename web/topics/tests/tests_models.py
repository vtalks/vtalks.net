from django.test import TestCase

from topics.models import Topic

# Create your tests here.


class TopicModelTests(TestCase):

    def setUp(self):
        Topic.objects.create(title='A Topic')
        Topic.objects.create(title='A Topic same title')
        Topic.objects.create(title='A Topic same title')

    def test_instance_get_string_repr(self):
        """ Topic object string representation returns its title
        """
        topic_1 = Topic.objects.get(title='A Topic')
        self.assertEquals(str(topic_1), topic_1.title)

    def test_create_duplicate_title_slug(self):
        topics = Topic.objects.filter(title='A Topic same title')
        self.assertEquals(len(topics), 2)
        self.assertEquals(topics[0].slug, 'a-topic-same-title-1')
