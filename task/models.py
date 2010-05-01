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







    

