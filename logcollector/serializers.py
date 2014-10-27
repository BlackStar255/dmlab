from django.forms import widgets
from rest_framework import serializers
from logcollector.models import Log

class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = ('timestamp', 'dim1', 'dim2', 'value')