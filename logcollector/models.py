from django.db import models

class Log(models.Model):
    timestamp = models.BigIntegerField()
    dim1 = models.IntegerField()
    dim2 = models.IntegerField()
    value = models.FloatField()    
    
    class Meta:
        ordering = ('timestamp',)