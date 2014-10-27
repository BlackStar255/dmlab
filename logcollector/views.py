from logcollector.models import Log
from logcollector.serializers import LogSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Max, Min, Avg, StdDev

class LogList(APIView):
    """
    List all logs, or create a new log.
    """
    def get(self, request, format=None):
        log = Log.objects.all()
        serializer = LogSerializer(log, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = LogSerializer(data=request.DATA, many = True)
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

    def put(self, request, pk, format=None):
        log = self.get_object(pk)
        serializer = LogSerializer(log, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        log = self.get_object(pk)
        log.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class LogMax(APIView):
    """
    Retrieve Max value between t1 and t2.
    """
    def get(self, request, ts1, ts2, dim1 = None, dim2 = None):
        rng = (ts1,ts2)
        data = Log.objects.all()
        if dim1 != None:
            data = data.filter(dim1 = dim1)
        if dim2 != None:
            data = data.filter(dim2 = dim2)
        data = data.filter(timestamp__range=rng)
        maximum = data.aggregate(Max('value'))
        return Response(maximum)

class LogMin(APIView):
    """
    Retrieve Min value between t1 and t2.
    """
    def get(self, request, ts1, ts2, dim1 = None, dim2 = None):
        rng = (ts1,ts2)
        data = Log.objects.all()
        if dim1 != None:
            data = data.filter(dim1 = dim1)
        if dim2 != None:
            data = data.filter(dim2 = dim2)
        data = data.filter(timestamp__range=rng)
        minimum = data.filter(timestamp__range=rng).aggregate(Min('value'))
        return Response(minimum)

class LogAvg(APIView):
    """
    Retrieve Avg value between t1 and t2.
    """
    def get(self, request, ts1, ts2, dim1 = None, dim2 = None):
        rng = (ts1,ts2)
        data = Log.objects.all()
        if dim1 != None:
            data = data.filter(dim1 = dim1)
        if dim2 != None:
            data = data.filter(dim2 = dim2)
        data = data.filter(timestamp__range=rng)
        avg = data.filter(timestamp__range=rng).aggregate(Avg('value'))
        return Response(avg)
        
class LogStdDev(APIView):
    """
    Retrieve Standard deviation for values between t1 and t2.
    """
    def get(self, request, ts1, ts2, dim1 = None, dim2 = None):
        rng = (ts1,ts2)
        data = Log.objects.all()
        if dim1 != None:
            data = data.filter(dim1 = dim1)
        if dim2 != None:
            data = data.filter(dim2 = dim2)
        data = data.filter(timestamp__range=rng)
        stddev = data.objects.filter(timestamp__range=rng).aggregate(StdDev('value'))
        return Response(stddev)
        
class LogMvgAvg(APIView):
    """
    Retrieve the n-element moving average for values between t1 and t2.
    """
    def get(self, request, ts1, ts2, n, dim1 = None, dim2 = None):
        rng = (ts1,ts2)
        data = Log.objects.all()
        if dim1 != None:
            data = data.filter(dim1 = dim1)
        if dim2 != None:
            data = data.filter(dim2 = dim2)
        data = data.filter(timestamp__range=rng)        
        mvgavg = data.filter(timestamp__range=rng).order_by('-timestamp')[:n].aggregate(Avg('value'))
        return Response(mvgavg)
        