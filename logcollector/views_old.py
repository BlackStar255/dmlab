from logcollector.models import Logcollector
from logcollector.serializers import LogcollectorSerializer
from rest_framework import generics
from django.db.models import Avg, Max


class LogcollectorList(generics.ListCreateAPIView):
    queryset = Logcollector.objects.all()
    serializer_class = LogcollectorSerializer


class LogcollectorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Logcollector.objects.all()
    serializer_class = LogcollectorSerializer
    
class LogcollectorMax(generics.ListAPIView):
   # serializer_class = LogcollectorSerializer
    def get_queryset(self):
        return Logcollector.objects.all().aggregate(Max('value'))
    
        