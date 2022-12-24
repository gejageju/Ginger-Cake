from django.db import models
from django.contrib.postgres.fields import ArrayField
# Create your models here.
from datetime import datetime
class Posts(models.Model):
    Title=models.CharField(max_length=255)
    description=models.TextField()
    tags = ArrayField(models.CharField(max_length=50),default=list)
    city=models.CharField(max_length=255)
    country=models.CharField(max_length=255)
    postedby=models.CharField(max_length=255)
    requests=ArrayField(models.CharField(max_length=255),default=list)
    date = models.DateTimeField(default=datetime.now)
    img = models.ImageField(upload_to='images/',blank=True)

class Room(models.Model):
    code=models.CharField(max_length=1000)
    users=ArrayField(models.CharField(max_length=255),default=list)

class Message(models.Model):
    value = models.CharField(max_length=1000000)
    date = models.DateTimeField(default=datetime.now, blank=True)
    user = models.CharField(max_length=1000000)
    room = models.CharField(max_length=1000000)   