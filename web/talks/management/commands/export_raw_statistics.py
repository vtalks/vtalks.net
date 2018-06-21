import csv

from django.core.management.base import BaseCommand

from ...models import Talk


class Command(BaseCommand):
    help = 'Export talks raw statistics to CSV.'

    def handle(self, *args, **options):
        talks = Talk.objects.all().order_by('id')
        with open('../talks_raw_stats.csv', 'w') as csvfile:
            fieldnames = ['id',
                          'code',
                          'youtube_views',
                          'youtube_likes',
                          'youtube_dislikes',
                          'youtube_favorites',
                          'views',
                          'likes',
                          'dislikes',
                          'favorites']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for talk in talks:
                writer.writerow({
                    'id': talk.id,
                    'code': talk.code,
                    'youtube_views': talk.youtube_view_count,
                    'youtube_likes': talk.youtube_like_count,
                    'youtube_dislikes': talk.youtube_dislike_count,
                    'youtube_favorites': talk.youtube_favorite_count,
                    'views': talk.view_count,
                    'likes': talk.like_count,
                    'dislikes': talk.dislike_count,
                    'favorites': talk.favorite_count,
                })
