# Create your views here.

from models import Checkout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.models import User 
from django.contrib.auth.decorators import login_required 
from django.contrib.gis.gdal import Envelope
from models import Checkout 



def tasks_json(request):
    # seems like there is a bug where it doesn't transform the geojson string 
    # need to do it manually for now 
    # this should also return 4326

    qs = Checkout.objects.all().transform(900913)

    for co in qs:
        #print co.geom.geojson
        co.geojson = co.geom.geojson



    return render_to_response("tasks.json", {"qs" : qs}, mimetype="application/json")




def checkout(request):
    
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/accounts/login/?next=%s' % request.path)

    if request.GET:
        if 'bbox' in request.GET:
            bbox = [ float(x) for x in request.GET['bbox'].split(",") ]
            # do a checkout of the bounding box 
            # must make sure its a valid boundingbox/polygon
            e = Envelope(bbox)
            c = Checkout()
            c.user = request.user
            c.geom = e.wkt 
            c.save()
            # needs to check to see if this overlaps with anyone elses checkout 
            return HttpResponse("Checkout complete: %s" % c.id )
        else:
            return HttpResponse("Need to include a bbox", status=405)
       
    else:
        return HttpResponse("Need to include a bbox", status=405)


def commit(request):
    return HttpResponse("Not Implemented", status=501)


def cancel(request):
    return HttpResponse("Not Implemented", status=501)


def index(request):
    return render_to_response("index.html")



    
