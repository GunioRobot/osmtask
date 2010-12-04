from django.contrib.gis import admin
from models import Checkout, Density




admin.site.register(Checkout, admin.OSMGeoAdmin)
admin.site.register(Density, admin.OSMGeoAdmin)


