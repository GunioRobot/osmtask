from lxml import etree
import sys
from django.contrib.gis.gdal import OGRGeometry

sys.path += "/Users/tlpinney/project/osmtask"
sys.path += "/Users/tlpinney/project/osmtask/task"
sys.path += "/Users/tlpinney/project"

import os
os.environ['PYTHONPATH'] = "/Users/tlpinney/project/osmtask"
os.environ['DJANGO_SETTINGS_MODULE'] = "settings"

from task.models import Density



#print sys.argv[1]

bottom = 4699912.2212166
left = -8586544.0162464
right = -8560612.7544053
top = 4708358.5128406


#bl = sys.argv[1].split(",")[:2]
#ur = sys.argv[1].split(",")[2:]

#print bl
#print ur

blah = "-77.1321,38.7965,-76.8993,39.0033"

bblah = [ float(i) for i in blah.split(",")]

Density.objects.all().delete()

foo = OGRGeometry.from_bbox(bblah)
#print foo
#foo.srid = 900913

#foo.transform(4326)
print foo

#import ipdb; ipdb.set_trace()


# from this figure out what would be the polygons in tile size 15
# from this a grid model can be created and can keep track of the amount of nodes per tile

# zoom level 0 is a 1x1 tile (256)
# zoom level 1 will have 4 tiles
# zoom level 2 will have 16 tles
# zoom level 3 will have 16^2
# etc

# this comes out to 2^2n
# depending on the extents, create the tiles

#lon/lat to tile number


extent = foo.extent

print extent


bl = extent[:2]
tr = extent[2:]

print bl
print tr

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



tlt = deg2num(bl[0], tr[1], 14)
trt = deg2num(tr[0], tr[1], 14)
tlb = deg2num(bl[0], bl[1], 14)

# get a list of all the tiles for the particular zoom level, scanning from left to right then going down
#print tlt
#print trt
#print tlb

xs = range(tlt[0], trt[0]+1)
ys = range(tlt[1], tlb[1]+1)

#print xs
#print ys

matrix = []
for xt in xs:
    for yt in  ys:
        matrix.append((xt, yt))


#print matrix

# need to get the bounding boxes of all of this tiles

tiles = 2**15

for foo in matrix:
    #91.02... tiles is one degree
    # what is the length of a tile in degrees?
    # 0.010986328125
    # find the start of the tile then create a bounding box of it
    # create an actual geometry from it, create the bbox
    #print foo[0]
    #print foo[0] *  0.010986328125
    #foo[1] = tiles - foo[1] 
    foo_1 = foo[1] 
    #print 2**15 
    #print foo[1]
    #print 2**15 - foo[1]
    #print (2**15 - foo[1]) *  0.0054931640625 - 90
    print foo[1]
    #sys.exit()
    
    #print foo[1] *  0.0054931640625
    bbox = (foo[0] * 0.02197265625 - 180, num2deg(foo[1] + 1), (foo[0] + 1) * 0.02197265625 - 180, num2deg(foo[1]))
    print bbox
    dens  = OGRGeometry.from_bbox(bbox)
    dens.srid = 4326
    #print dens
    d = Density()
    #print d
    d.x = foo[0]
    d.y = foo[1]
    d.geom = dens.wkt
    d.save()
    

    # save the geometries to the new density model
    
    







# convert to lat long




