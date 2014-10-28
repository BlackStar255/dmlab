# -*- coding: utf-8 -*-
from logcollector.models import Log
from logcollector.serializers import LogSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Max, Min, Avg, StdDev

class LogFun(APIView):
    
    def get(self, request, format=None):
        params = request.GET
        method = None
        if 't1' not in params.keys() or 't2' not in params.keys():
            log = Log.objects.all().order_by('-timestamp')[:5]
            serializer = LogSerializer(log, many=True)
            return Response(serializer.data)
        rng = (params['t1'],params['t2'])
        if 'method' in params.keys():
            method = params['method']
        
        #Checking for optional parameters and filter the data
        if 'dim1' in params.keys():
            dim1 = params['dim1']
            data = Log.objects.filter(dim1 = dim1)
        if 'dim2' in params.keys():
            dim2 = params['dim2']
            if 'data' in locals():
                data = data.filter(dim2 = dim2)
            else: 
                data = Log.objects.filter(dim2 = dim2)
                
        #Calculate the required data
        if method == 'Min':
            if 'data' in locals():
                minimum = data.filter(timestamp__range=rng).aggregate(Min('value'))['value__min']
            else:
                minimum = Log.objects.filter(timestamp__range=rng).aggregate(Min('value'))['value__min']
            return Response(minimum)
        elif method == 'Max':
            if 'data' in locals():
                maximum = data.filter(timestamp__range=rng).aggregate(Max('value'))['value__max']
            else:
                maximum = Log.objects.filter(timestamp__range=rng).aggregate(Max('value'))['value__max']
            return Response(maximum)
        elif method == 'Avg':
            if 'data' in locals():
                avg = data.filter(timestamp__range=rng).aggregate(Avg('value'))['value__avg']
            else:
                avg = Log.objects.filter(timestamp__range=rng).aggregate(Avg('value'))['value__avg']
            return Response(avg)
        elif method == 'StdDev':
            if 'data' in locals():
                stddev = data.filter(timestamp__range=rng).aggregate(StdDev('value'))['value__stddev']
            else:
                stddev = Log.objects.filter(timestamp__range=rng).aggregate(StdDev('value'))['value__stddev']
            return Response(stddev)
        elif method == 'MvgAvg':
            n = 5
            if 'n' in params.keys():
                n = params['n']
            if 'data' in locals():
                mvgavg = data.filter(timestamp__range=rng).aggregate(Avg('value'))['value__avg']
            else:
                mvgavg = Log.objects.filter(timestamp__range=rng).order_by('-timestamp')[:n].aggregate(Avg('value'))['value__avg']
            return Response(mvgavg)
    

    def post(self, request, format=None):
        serializer = LogSerializer(data=request.DATA, many = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)            
    
"""
class LogDetail(APIView):
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
        
class LogList(APIView):
     def get(self, request, format=None):
        log = Log.objects.all()
        serializer = LogSerializer(log, many=True)
        return Response(serializer.data)
        
"""