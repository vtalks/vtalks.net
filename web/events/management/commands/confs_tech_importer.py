import requests

from django.utils import timezone
from django.core.management.base import BaseCommand

from events.management import utils

from events.models import Event
from events.models import Edition


class Command(BaseCommand):
    help = 'Import events from a confs.tech json file to the database.'

    source_urls = {}
    source_urls["2014"] = [
        "https://raw.githubusercontent.com/tech-conferences/confs.tech/master/conferences/2014/ruby.json",
        "https://raw.githubusercontent.com/tech-conferences/confs.tech/master/conferences/2014/ux.json",
    ]
    """
    source_urls["2015"] = [
        "https://raw.githubusercontent.com/tech-conferences/confs.tech/master/conferences/2015/ruby.json",
        "https://raw.githubusercontent.com/tech-conferences/confs.tech/master/conferences/2015/ux.json",
    ]
    source_urls["2016"] = [
        "https://raw.githubusercontent.com/tech-conferences/confs.tech/master/conferences/2016/ruby.json",
        "https://raw.githubusercontent.com/tech-conferences/confs.tech/master/conferences/2016/ux.json",
    ]
    source_urls["2017"] = [
        "https://raw.githubusercontent.com/tech-conferences/confs.tech/master/conferences/2017/android.json",
        "https://raw.githubusercontent.com/tech-conferences/confs.tech/master/conferences/2017/css.json",
        "https://raw.githubusercontent.com/tech-conferences/confs.tech/master/conferences/2017/data.json",
        "https://raw.githubusercontent.com/tech-conferences/confs.tech/master/conferences/2017/devops.json",
        "https://raw.githubusercontent.com/tech-conferences/confs.tech/master/conferences/2017/general.json",
        "https://raw.githubusercontent.com/tech-conferences/confs.tech/master/conferences/2017/ios.json",
        "https://raw.githubusercontent.com/tech-conferences/confs.tech/master/conferences/2017/php.json",
        "https://raw.githubusercontent.com/tech-conferences/confs.tech/master/conferences/2017/ruby.json",
        "https://raw.githubusercontent.com/tech-conferences/confs.tech/master/conferences/2017/tech-comm.json",
        "https://raw.githubusercontent.com/tech-conferences/confs.tech/master/conferences/2017/ux.json",
    ]
    source_urls["2018"] = [
        "https://raw.githubusercontent.com/tech-conferences/confs.tech/master/conferences/2018/android.json",
        "https://raw.githubusercontent.com/tech-conferences/confs.tech/master/conferences/2018/css.json",
        "https://raw.githubusercontent.com/tech-conferences/confs.tech/master/conferences/2018/data.json",
        "https://raw.githubusercontent.com/tech-conferences/confs.tech/master/conferences/2018/devops.json",
        "https://raw.githubusercontent.com/tech-conferences/confs.tech/master/conferences/2018/dotnet.json",
        "https://raw.githubusercontent.com/tech-conferences/confs.tech/master/conferences/2018/elixir.json",
        "https://raw.githubusercontent.com/tech-conferences/confs.tech/master/conferences/2018/general.json",
        "https://raw.githubusercontent.com/tech-conferences/confs.tech/master/conferences/2018/golang.json",
        "https://raw.githubusercontent.com/tech-conferences/confs.tech/master/conferences/2018/ios.json",
        "https://raw.githubusercontent.com/tech-conferences/confs.tech/master/conferences/2018/php.json",
        "https://raw.githubusercontent.com/tech-conferences/confs.tech/master/conferences/2018/python.json",
        "https://raw.githubusercontent.com/tech-conferences/confs.tech/master/conferences/2018/ruby.json",
        "https://raw.githubusercontent.com/tech-conferences/confs.tech/master/conferences/2018/rust.json",
        "https://raw.githubusercontent.com/tech-conferences/confs.tech/master/conferences/2018/scala.json",
        "https://raw.githubusercontent.com/tech-conferences/confs.tech/master/conferences/2018/security.json",
        "https://raw.githubusercontent.com/tech-conferences/confs.tech/master/conferences/2018/tech-comm.json",
        "https://raw.githubusercontent.com/tech-conferences/confs.tech/master/conferences/2018/ux.json",
    ]
    source_urls["2019"] = [
        "https://raw.githubusercontent.com/tech-conferences/confs.tech/master/conferences/2019/android.json",
        "https://raw.githubusercontent.com/tech-conferences/confs.tech/master/conferences/2019/css.json",
        "https://raw.githubusercontent.com/tech-conferences/confs.tech/master/conferences/2019/data.json",
        "https://raw.githubusercontent.com/tech-conferences/confs.tech/master/conferences/2019/devops.json",
        "https://raw.githubusercontent.com/tech-conferences/confs.tech/master/conferences/2019/elixir.json",
        "https://raw.githubusercontent.com/tech-conferences/confs.tech/master/conferences/2019/general.json",
        "https://raw.githubusercontent.com/tech-conferences/confs.tech/master/conferences/2019/golang.json",
        "https://raw.githubusercontent.com/tech-conferences/confs.tech/master/conferences/2019/ios.json",
        "https://raw.githubusercontent.com/tech-conferences/confs.tech/master/conferences/2019/php.json",
        "https://raw.githubusercontent.com/tech-conferences/confs.tech/master/conferences/2019/python.json",
        "https://raw.githubusercontent.com/tech-conferences/confs.tech/master/conferences/2019/ruby.json",
        "https://raw.githubusercontent.com/tech-conferences/confs.tech/master/conferences/2019/rust.json",
        "https://raw.githubusercontent.com/tech-conferences/confs.tech/master/conferences/2019/security.json",
        "https://raw.githubusercontent.com/tech-conferences/confs.tech/master/conferences/2019/tech-comm.json",
        "https://raw.githubusercontent.com/tech-conferences/confs.tech/master/conferences/2019/ux.json",
    ]
    """

    def add_arguments(self, parser):
        pass

    def create_event_edition(self, event_json_data, year, event):
        """ Create an event edition
        """
        event_edition_name = ""
        if "name" in event_json_data:
            event_edition_name = "{:s} {:s}".format(event_json_data["name"], year)

        event_edition_url = ""
        if "url" in event_json_data:
            event_edition_url = event_json_data['url']

        event_edition_country = ""
        if "country" in event_json_data:
            event_edition_country = event_json_data['country']

        event_edition_city = ""
        if "city" in event_json_data:
            event_edition_city = event_json_data['city']

        event_edition = Edition.objects.create(title=event_edition_name,
                                               url=event_edition_url,
                                               country=event_edition_country,
                                               city=event_edition_city,
                                               event=event,
                                               created=timezone.now())
        return event_edition

    def update_event_edition(self, event_json_data, year, event):
        """ Update an event edition
        """
        event_edition_name = ""
        if "name" in event_json_data:
            event_edition_name = "{:s} {:s}".format(event_json_data["name"], year)

        event_edition_url = ""
        if "url" in event_json_data:
            event_edition_url = event_json_data['url']

        event_edition_country = ""
        if "country" in event_json_data:
            event_edition_country = event_json_data['country']

        event_edition_city = ""
        if "city" in event_json_data:
            event_edition_city = event_json_data['city']

        event_edition = Edition.objects.get(title=event_edition_name)
        event_edition.title = event_edition_name
        event_edition.url = event_edition_url
        event_edition.country = event_edition_country
        event_edition.city = event_edition_city
        event_edition.event = event
        event_edition.save()

        return event_edition

    def update_event(self, event_json_data):
        """ Update an event
        """
        event_name = ""
        if "name" in event_json_data:
            event_name = event_json_data["name"]

        event_twitter_handle = ""
        if "twitter" in event_json_data:
            event_twitter_handle = utils.get_twitter_handle(event_json_data['twitter'])

        event_url = ""
        if "url" in event_json_data:
            event_url = event_json_data['url']

        event = Event.objects.get(title=event_name)
        event.title = event_name
        event.twitter = event_twitter_handle
        event.url = event_url
        event.save()

        return event

    def create_event(self, event_json_data):
        """ Create an event
        """
        event_name = ""
        if "name" in event_json_data:
            event_name = event_json_data["name"]

        event_twitter_handle = ""
        if "twitter" in event_json_data:
            event_twitter_handle = utils.get_twitter_handle(event_json_data['twitter'])

        event_url = ""
        if "url" in event_json_data:
            event_url = event_json_data['url']

        event = Event.objects.create(title=event_name,
                                     twitter=event_twitter_handle,
                                     url=event_url,
                                     created=timezone.now())
        return event

    def handle(self, *args, **options):
        for source_urls_year in self.source_urls:
            print("Importing {:s} conferences ...".format(source_urls_year))

            for source_url in self.source_urls[source_urls_year]:
                input_json_data = requests.get(source_url).json()

                for event_json_data in input_json_data:

                    # create or update Event
                    event_name = ""
                    if "name" in event_json_data:
                        event_name = event_json_data["name"]

                    event = None
                    if not Event.objects.filter(title=event_name).exists():
                        event = self.create_event(event_json_data)
                        print("Event {:d} - {:s} created successfully".format(event.id, event.title))
                    else:
                        event = self.update_event(event_json_data)
                        print("Event {:d} - {:s} updated successfully".format(event.id, event.title))

                    # create or update Event Edition
                    event_edition_name = "{:s} {:s}".format(event_name, source_urls_year)

                    event_edition = None
                    if not Edition.objects.filter(title=event_edition_name).exists():
                        event_edition = self.create_event_edition(event_json_data, source_urls_year, event)
                        print("Event Edition {:d} - {:s} created successfully".format(event_edition.id, event_edition.title))
                    else:
                        event_edition = self.update_event_edition(event_json_data, source_urls_year, event)
                        print("Event Edition {:d} - {:s} updated successfully".format(event_edition.id, event_edition.title))
