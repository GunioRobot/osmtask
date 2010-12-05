from django.contrib.gis.db import models
from django.contrib.auth.models import User


# Create your models here.


class Checkout(models.Model):
    user = models.ForeignKey(User)
    geom = models.PolygonField(srid=4326) # bounding box of checked out area
    canceled = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = models.GeoManager()


class Commit(models.Model):
    checkout = models.ForeignKey(Checkout)
    osm = models.XMLField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = models.GeoManager()


class Density(models.Model):
    geom = models.PolygonField(srid=4326)
    x = models.IntegerField()
    y = models.IntegerField()
    z = models.IntegerField(default=15)
    density = models.IntegerField(default=0)
    objects = models.GeoManager()

class Task(models.Model):
    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=50,null=True)
    description = models.CharField(max_length=1024)
    geom = models.PolygonField(srid=4326)
    objects = models.GeoManager()
    def __unicode__(self):
        return self.title
    


class TaskCell(models.Model):
    geom = models.PolygonField(srid=4326)
    x = models.IntegerField()
    y = models.IntegerField()
    z = models.IntegerField(default=15)
    task = models.ForeignKey(Task)
    objects = models.GeoManager()

    




    

