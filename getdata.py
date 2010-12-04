from lxml import etree
import sys
from django.contrib.gis.gdal import OGRGeometry
import httplib2

sys.path += "/Users/tlpinney/project/osmtask"
sys.path += "/Users/tlpinney/project/osmtask/task"
sys.path += "/Users/tlpinney/project"

import os
os.environ['PYTHONPATH'] = "/Users/tlpinney/project/osmtask"
os.environ['DJANGO_SETTINGS_MODULE'] = "settings"

from task.models import Density


qs = Density.objects.all()

from lxml import etree


for d in qs:
    e = d.geom.extent
    h = httplib2.Http()
    resp, content = h.request("http://api.openstreetmap.org/api/0.6/map?bbox=%s,%s,%s,%s" % (e[0],e[1],e[2],e[3]) )
    print content
    root = etree.fromstring(content)
    density = len(root.findall("node"))
    d.density = density
    d.save()
    




