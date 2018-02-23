import plotly.plotly as py
import plotly.graph_objs as go

from django.core.management.base import BaseCommand

from ...models import Talk


class Command(BaseCommand):
    help = 'Calculates the rank of videos based on its upvotes & downvotes.'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        py.sign_in('vtalks', 'BcoUuEPfaqc3xGcPyU3l')

        # Wilson Score plot

        talks = Talk.objects.all().order_by('-wilsonscore_rank')
        ids = []
        wilson_scores = []

        for talk in talks:
            ids.append("id:"+str(talk.id))
            wilson_scores.append(talk.wilsonscore_rank)

        data = [go.Bar(
            x=ids,
            y=wilson_scores
        )]

        py.plot(data, filename='wilsonscore-bar')

        # Hacker hot plot

        talks = Talk.objects.all().order_by('-hacker_hot')
        ids = []
        hacker_scores = []

        for talk in talks:
            ids.append("id:" + str(talk.id))
            hacker_scores.append(talk.hacker_hot)

        data = [go.Bar(
            x=ids,
            y=hacker_scores
        )]

        py.plot(data, filename='hackerhot-bar')
