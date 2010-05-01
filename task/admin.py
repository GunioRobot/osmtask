from django.contrib.gis import admin
from models import Checkout


admin.site.register(Checkout, admin.GeoModelAdmin)

