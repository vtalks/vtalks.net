import requests

from django.core.management.base import BaseCommand

from events.models import Event
from events.models import Edition
from events.management import event
from events.management import edition

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

                    if not Event.objects.filter(title=event_name).exists():
                        event_obj = event.create_event(event_json_data)
                        print("Event {:d} - {:s} created successfully".format(event_obj.id, event_obj.title))
                    else:
                        event_obj = event.update_event(event_json_data)
                        event_obj.save()
                        print("Event {:d} - {:s} updated successfully".format(event_obj.id, event_obj.title))

                    # create or update Event Edition
                    event_edition_name = "{:s} {:s}".format(event_name, source_urls_year)

                    if not Edition.objects.filter(title=event_edition_name).exists():
                        event_edition_obj = edition.create_event_edition(event_json_data, source_urls_year, event_obj)
                        print("Event Edition {:d} - {:s} created successfully".format(event_edition_obj.id, event_edition_obj.title))
                    else:
                        event_edition_obj = edition.update_event_edition(event_json_data, source_urls_year, event_obj)
                        event_edition_obj.save()
                        print("Event Edition {:d} - {:s} updated successfully".format(event_edition_obj.id, event_edition_obj.title))
