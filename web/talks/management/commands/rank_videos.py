from django.utils import timezone

from django.core.management.base import BaseCommand

from ...models import Talk
from ...decay import popularity


class Command(BaseCommand):
    help = 'Calculates the rank of videos based on its upvotes & downvotes.'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        talks = Talk.objects.all().order_by('updated')
        for talk in talks:
            wilsonscore_rank = popularity.wilson_score(talk.total_like_count, talk.total_dislike_count)

            votes = abs(talk.total_like_count - talk.total_dislike_count)
            hacker_hot = popularity.hacker_hot(votes, talk.created)

            talk.updated = timezone.now()

            self.stdout.write(self.style.SUCCESS('Rank for "%s"' % talk.title))
            self.stdout.write('\tVotes: (+%d/-%d)' % (talk.youtube_like_count, talk.youtube_dislike_count))
            self.stdout.write('\tWilsonScore rank: %f ' % wilsonscore_rank)
            self.stdout.write('\tViews: %d' % talk.youtube_view_count)
            self.stdout.write('\tHackerNews hot rank: %f' % hacker_hot)

            talk.save()
