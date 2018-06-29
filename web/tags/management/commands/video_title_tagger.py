from django.core.management.base import BaseCommand

from talks.models import Talk


class Command(BaseCommand):
    help = 'Search on video titles for a keyword and tag them with it.'

    def add_arguments(self, parser):
        parser.add_argument('keyword', type=str)

    def handle(self, *args, **options):
        keyword = options["keyword"]

        # Search on video titles for this keyword
        talks = Talk.objects.filter(title__icontains=" "+keyword+" ").all().order_by("id")

        print("Searching talks for keyword:{:s}, found {:d} videos".format(keyword, talks.count()))

        for talk in talks:
            talk.tags.add(keyword)
            talk.save()
            print("Tagged video id:{:d} - code:{:s} - title:{:s}, as {:s}".format(talk.id, talk.code, talk.title, keyword))