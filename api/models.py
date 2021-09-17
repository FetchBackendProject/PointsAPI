from django.db import models

class person(models.Model):
    payer = models.CharField(max_length=100)
    points = models.IntegerField()
    timestamp = models.DateField()