from django.core.management.base import BaseCommand

from ...models import Talk
from ...decay import popularity


class Command(BaseCommand):
    help = 'Dumps the rank of the video.'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        talks = Talk.objects.all()
        for talk in talks:
            wilsonscore_rank = popularity.wilson_score(talk.like_count, talk.dislike_count)
            talk.wilsonscore_rank = wilsonscore_rank

            hacker_hot = popularity.hacker_hot(talk.view_count, talk.created)
            talk.hacker_hot = hacker_hot

            talk.save()
