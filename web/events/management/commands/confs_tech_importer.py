import requests

from django.core.management.base import BaseCommand

from events.models import Event
from events.models import Edition
from events.management import event
from events.management import edition
from events.management.sources import source_urls



class Command(BaseCommand):
    help = 'Import events from a confs.tech json file to the database.'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        for source_urls_year in source_urls:
            print("Importing {:s} conferences ...".format(source_urls_year))

            for source_url in source_urls[source_urls_year]:
                input_json_data = requests.get(source_url).json()

                for event_json_data in input_json_data:

                    # create or update Event
                    event_name = ""
                    if "name" in event_json_data:
                        event_name = event_json_data["name"]

                    if not Event.objects.filter(title=event_name).exists():
                        event_obj = event.create_event(event_json_data)
                        msg = "Event {:d} - {:s} created successfully".format(event_obj.id, event_obj.title)
                        print(msg)
                    else:
                        event_obj = event.update_event(event_json_data)
                        event_obj.save()
                        msg = "Event {:d} - {:s} updated successfully".format(event_obj.id, event_obj.title)
                        print(msg)


                    # create or update Event Edition
                    event_edition_name = "{:s} {:s}".format(event_name, source_urls_year)

                    if not Edition.objects.filter(title=event_edition_name).exists():
                        event_edition_obj = edition.create_event_edition(event_json_data, source_urls_year, event_obj)
                        msg = "Event Edition {:d} - {:s} created successfully".format(event_edition_obj.id, event_edition_obj.title)
                        print(msg)
                    else:
                        event_edition_obj = edition.update_event_edition(event_json_data, source_urls_year, event_obj)
                        event_edition_obj.save()
                        msg = "Event Edition {:d} - {:s} updated successfully".format(event_edition_obj.id, event_edition_obj.title)
                        print(msg)

