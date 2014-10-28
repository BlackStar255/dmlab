# -*- coding: utf-8 -*-
from logcollector.models import Log
from logcollector.serializers import LogSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Max, Min, Avg, StdDev


def check_int_value(value):
    try:
        int(value)
    except ValueError:
        return Response(status=status.HTTP_400_BAD_REQUEST)

class LogFun(APIView):

    def get(self, request, format=None):
        #List the last 5 log instance, or calculate the required data based on the parameters of the get request
        params = request.GET
        method = None
        
        #List the last five log instance if t1 or t2 not provided    
        if 't1' not in params.keys() or 't2' not in params.keys():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        rng = (params['t1'],params['t2'])
        check_int_value(rng[0])
        check_int_value(rng[1])       
        
        #Checking for optional dim1, dim2 parameters and filter the data
        data = Log.objects.all()
        if 'dim1' in params:
            dim1 = params['dim1']
            check_int_value(dim1)
            data = data.filter(dim1 = dim1)

        if 'dim2' in params:
            dim2 = params['dim2']
            check_int_value(dim2)
            data = data.filter(dim2 = dim2)               
                
        #Setting the method
        if 'method' in params:
            method = params['method']
        
        #Calculate the required data
        if method == 'Min':
            minimum = data.filter(timestamp__range=rng).aggregate(Min('value'))['value__min']
            return Response(minimum)
        elif method == 'Max':
            maximum = data.filter(timestamp__range=rng).aggregate(Max('value'))['value__max']
            return Response(maximum)
        elif method == 'Avg':
            avg = data.filter(timestamp__range=rng).aggregate(Avg('value'))['value__avg']
            return Response(avg)
        elif method == 'StdDev':
            stddev = data.filter(timestamp__range=rng).aggregate(StdDev('value',sample=True))['value__stddev']
            if not stddev:
                return Response(0.0) #Database doesn't calculate stddev on one-element input                
            return Response(stddev)
        elif method == 'MvgAvg':
            n = None             
            if 'n' in params:
                n = params['n']
                check_int_value(n)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            mvgavg = data.filter(timestamp__range=rng).order_by('-timestamp')[:n].aggregate(Avg('value'))['value__avg']
            return Response(mvgavg)
        else:
             return Response(status=status.HTTP_400_BAD_REQUEST)                       
    

    def post(self, request, format=None):
        #Create a new log instance
        serializer = LogSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)            