import logging
import csv
import datetime

from django.utils import timezone
from django.core.management.base import BaseCommand

from talks.models import Talk


class Command(BaseCommand):
    help = 'Exports a data set of talks to CSV.'

    def export_data(self, talks, path):
        with open(path, 'w', newline='') as csvfile:
            fieldnames = ['id',
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

    def handle(self, *args, **options):
        # Export complete data set
        print("Generating all dataset ...")
        talks = Talk.published_objects.all().order_by('id')
        self.export_data(talks, '/.dataset/vtalks_dataset_all.csv')

        # Export data set per year
        years = list(range(2018, 2009, -1))
        for year in years:
            print("Generating {:d} dataset ...".format(year))
            start_year = datetime.datetime(year, 1, 1, 0, 0, 0).replace(tzinfo=timezone.utc)
            end_year = datetime.datetime(year, 12, 31, 23, 59, 59).replace(tzinfo=timezone.utc)
            talks = Talk.published_objects.filter(created__gte=start_year, created__lte=end_year)
            path = '/.dataset/vtalks_dataset_{:d}.csv'.format(year)
            self.export_data(talks, path)





