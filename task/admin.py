from django.contrib.gis import admin
from models import Checkout, Density, Task

class DensityAdmin(admin.OSMGeoAdmin):
    list_display = ('id','x','y','z','density')
    
class TaskAdmin(admin.OSMGeoAdmin):
    list_display = ('id','title','description')


admin.site.register(Checkout, admin.OSMGeoAdmin)
admin.site.register(Density, DensityAdmin)
admin.site.register(Task, TaskAdmin)




