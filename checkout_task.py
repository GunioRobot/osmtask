from lxml import etree
import sys
from django.contrib.gis.gdal import OGRGeometry

sys.path += "/Users/tlpinney/project/osmtask"
sys.path += "/Users/tlpinney/project/osmtask/task"
sys.path += "/Users/tlpinney/project"

import os
os.environ['PYTHONPATH'] = "/Users/tlpinney/project/osmtask"
os.environ['DJANGO_SETTINGS_MODULE'] = "settings"

from task.models import TaskCell
from task.models import Task



qs = Task.objects.all()

import math
def deg2num(lon_deg, lat_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
    return(xtile, ytile)


def num2deg(xtile, ytile, zoom):
   n = 2.0 ** zoom
   lon_deg = xtile / n * 360.0 - 180.0
   lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
   lat_deg = math.degrees(lat_rad)
   return(lat_deg, lon_deg)

def num2deg(ytile):
   n = 2.0 ** 14
   lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
   lat_deg = math.degrees(lat_rad)
   return lat_deg


for t in qs:
    extent = t.geom.extent
    print extent
    bl = extent[:2]
    tr = extent[2:]

    tlt = deg2num(bl[0], tr[1], 14)
    trt = deg2num(tr[0], tr[1], 14)
    tlb = deg2num(bl[0], bl[1], 14)

    xs = range(tlt[0], trt[0]+1)
    ys = range(tlt[1], tlb[1]+1)

    matrix = []
    for xt in xs:
        for yt in  ys:
            matrix.append((xt, yt))

    for foo in matrix:
        foo_1 = foo[1]     
        bbox = (foo[0] * 0.02197265625 - 180, num2deg(foo[1] + 1), (foo[0] + 1) * 0.02197265625 - 180, num2deg(foo[1]))
        print bbox
        dens  = OGRGeometry.from_bbox(bbox)
        dens.srid = 4326
        d = TaskCell()
        d.x = foo[0]
        d.y = foo[1]
        d.geom = dens.wkt
        d.task = t
        d.save()
    

