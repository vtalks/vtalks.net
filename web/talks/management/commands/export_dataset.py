import csv

from django.core.management.base import BaseCommand

from talks.models import Talk


class Command(BaseCommand):
    help = 'Exports a data set of talks to CSV.'

    def handle(self, *args, **options):
        talks = Talk.published_objects.all().order_by('id')
        with open('/.dataset/vtalks_dataset.csv', 'w', newline='') as csvfile:
            fieldnames = ['id',
                          'code',
                          'created',
                          'youtube_view_count',
                          'youtube_like_count',
                          'youtube_dislike_count',
                          'youtube_favorite_count',
                          'view_count',
                          'like_count',
                          'dislike_count',
                          'favorite_count']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for talk in talks:
                writer.writerow({
                    'id': talk.id,
                    'code': talk.code,
                    'created': talk.created,
                    'youtube_view_count': talk.youtube_view_count,
                    'youtube_like_count': talk.youtube_like_count,
                    'youtube_dislike_count': talk.youtube_dislike_count,
                    'youtube_favorite_count': talk.youtube_favorite_count,
                    'view_count': talk.view_count,
                    'like_count': talk.like_count,
                    'dislike_count': talk.dislike_count,
                    'favorite_count': talk.favorite_count
                })


