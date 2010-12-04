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

print qs

d = qs[0]

# make a request to OSM to retrieve the data for the first square


