from django.contrib.gis import admin
from models import Checkout, Density

class DensityAdmin(admin.OSMGeoAdmin):
    list_display = ('id','x','y','z','density')
    


admin.site.register(Checkout, admin.OSMGeoAdmin)
admin.site.register(Density, DensityAdmin)


