from logcollector.models import Log
from logcollector.serializers import LogSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Max, Min, Avg, StdDev

class LogList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        log = Log.objects.all()
        serializer = LogSerializer(log, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = LogSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
    
class LogDetail(APIView):
    """
    Retrieve a log instance.
    """
    def get_object(self, pk):
        try:
            return Log.objects.get(timestamp=pk)
        except Log.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        log = self.get_object(pk)
        serializer = LogSerializer(log)
        return Response(serializer.data)

class LogMax(APIView):
    """
    Retrieve Max value between t1 and t2.
    """
    def get(self, request, pk1, pk2):
        start = pk1
        stop = pk2
        maximum = Log.objects.filter(timestamp__range=(start,stop)).aggregate(Max('value'))
        return Response(maximum)

class LogMin(APIView):
    """
    Retrieve Min value between t1 and t2.
    """
    def get(self, request, pk1, pk2):
        start = pk1
        stop = pk2
        minimum = Log.objects.filter(timestamp__range=(start,stop)).aggregate(Min('value'))
        return Response(minimum)

class LogAvg(APIView):
    """
    Retrieve Avg value between t1 and t2.
    """
    def get(self, request, pk1, pk2):
        start = pk1
        stop = pk2
        avg = Log.objects.filter(timestamp__range=(start,stop)).aggregate(Avg('value'))
        return Response(avg)
        
class LogStdDev(APIView):
    """
    Retrieve Standard deviation for values between t1 and t2.
    """
    def get(self, request, pk1, pk2):
        start = pk1
        stop = pk2
        stddev = Log.objects.filter(timestamp__range=(start,stop)).aggregate(StdDev('value'))
        return Response(stddev)
        
class LogMvgAvg(APIView):
    """
    Retrieve the n-element moving average for values between t1 and t2.
    """
    def get(self, request, pk1, pk2, n):
        start = pk1
        stop = pk2
        
        mvgavg = Log.objects.filter(timestamp__range=(start,stop)).order_by('-timestamp')[:n].aggregate(Avg('value'))
        return Response(mvgavg)
        