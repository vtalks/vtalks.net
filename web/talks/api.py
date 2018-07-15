from datetime import date
from dateutil.relativedelta import relativedelta

from rest_framework import viewsets
from rest_framework import views
from rest_framework.response import Response

from .models import Talk

from .serializers import TalkSerializer


class TalkViewSet(viewsets.ModelViewSet):
    queryset = Talk.objects.all()
    serializer_class = TalkSerializer


class RandomTalkView(views.APIView):

    def get(self, request, format=None):
        """ Get a random Talk object created no earlier than six months ago
        """
        today = date.today()
        six_months_ago = today - relativedelta(months=6)

        talk = Talk.objects.filter(created__gte=six_months_ago).order_by('?').first()

        serializer = TalkSerializer(talk, many=False)
        return Response(serializer.data)
