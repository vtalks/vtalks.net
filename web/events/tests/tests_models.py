from django.test import TestCase

from events.models import Event
from events.models import Edition

# Create your tests here.


class EventModelTests(TestCase):

    def setUp(self):
        Event.objects.create(title='event title 1')
        Event.objects.create(title='event title same title')
        Event.objects.create(title='event title same title')

    def test_instance_get_string_repr(self):
        event_1 = Event.objects.get(id='1')
        self.assertEquals(str(event_1), event_1.title)

    def test_create_duplicate_title_slug(self):
        event_12 = Event.objects.get(id='3')
        self.assertEquals(event_12.slug, 'event-title-same-title-1')


class EditionModelTests(TestCase):

    def setUp(self):
        event_1 = Event.objects.create(title='edition title 1')
        Edition.objects.create(title='edition title 1', event=event_1)
        Edition.objects.create(title='edition title same title', event=event_1)
        Edition.objects.create(title='edition title same title', event=event_1)

    def test_instance_get_string_repr(self):
        edition_1 = Edition.objects.get(id='1')
        self.assertEquals(str(edition_1), edition_1.title)

    def test_create_duplicate_title_slug(self):
        edition_12 = Edition.objects.get(id='3')
        self.assertEquals(edition_12.slug, 'edition-title-same-title-1')

    def test_save_edition_slug(self):
        edition_1 = Edition.objects.get(id=1)
        edition_1.title = "another edition"
        edition_1.save()
        self.assertEquals(edition_1.slug, 'edition-title-1')