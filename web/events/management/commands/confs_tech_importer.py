import requests

from django.utils import timezone
from django.core.management.base import BaseCommand

from events.models import Event


class Command(BaseCommand):
    help = 'Import events from a confs.tech json file to the database.'

    source_urls = [
        "https://raw.githubusercontent.com/tech-conferences/confs.tech/master/conferences/2014/ruby.json",
        "https://raw.githubusercontent.com/tech-conferences/confs.tech/master/conferences/2014/ux.json",

        "https://raw.githubusercontent.com/tech-conferences/confs.tech/master/conferences/2015/ruby.json",
        "https://raw.githubusercontent.com/tech-conferences/confs.tech/master/conferences/2015/ux.json",

        "https://raw.githubusercontent.com/tech-conferences/confs.tech/master/conferences/2016/ruby.json",
        "https://raw.githubusercontent.com/tech-conferences/confs.tech/master/conferences/2016/ux.json",

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

    def add_arguments(self, parser):
        pass

    def update_event(self, event_json_data):
        """ Update an event to the database
        """
        event_name = ""
        if "name" in event_json_data:
            event_name = event_json_data["name"]

        event = Event.objects.get(title=event_name)
        return event

    def create_event(self, event_json_data):
        """ Create a new event to the database
        """
        event_name = ""
        if "name" in event_json_data:
            event_name = event_json_data["name"]

        event_twitter_handle = ""
        if "twitter" in event_json_data:
            if event_json_data['twitter']:
                try:
                    event_twitter_handle = str.split(event_json_data['twitter'], ',')[1]
                except IndexError:
                    event_twitter_handle = str.lstrip(event_json_data['twitter'], '@')

        event_url = ""
        if "url" in event_json_data:
            event_url = event_json_data['url']

        event = Event.objects.create(title=event_name,
                                     url=event_url,
                                     twitter=event_twitter_handle,
                                     created=timezone.now())
        return event

    def handle(self, *args, **options):
        for source_url in self.source_urls:
            input_json_data = requests.get(source_url).json()

            for event_json_data in input_json_data:
                if not Event.objects.filter(title=event_json_data['name']).exists():
                    event = self.create_event(event_json_data)
                    print("Event {:d} - {:s} created successfully".format(event.id, event.title))
                else:
                    event = self.update_event(event_json_data)
                    print("Event {:d} - {:s} updated successfully".format(event.id, event.title))
