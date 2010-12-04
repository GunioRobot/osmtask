from django.contrib.gis import admin
from models import Checkout, Density, Task, TaskCell


class DensityAdmin(admin.OSMGeoAdmin):
    list_display = ('id','x','y','z','density')
    
class TaskAdmin(admin.OSMGeoAdmin):
    list_display = ('id','title','description')

class TaskCellAdmin(admin.OSMGeoAdmin):
    list_display = ('id', 'task','x', 'y', 'z')
    

admin.site.register(Checkout, admin.OSMGeoAdmin)
admin.site.register(Density, DensityAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(TaskCell, TaskCellAdmin)




