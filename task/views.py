# Create your views here.

from models import Checkout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.models import User 
from django.contrib.auth.decorators import login_required 
from django.contrib.gis.gdal import Envelope
from models import Checkout, Density, Task, TaskCell



#from django.contrib.gis.feeds import Feed



#class CheckoutFeed(Feed):   
#    title = "Checkout"
#    link = "/feed"
#    description = "Updates on changes in checkouts"
    
#    def items(self):
#        return Ch

    
#    def item_geometry(self, obj):
#        return obj.geom
    


def task(request, id):
    id = int(id)
    if request.method == 'DELETE':
        print "requesting a delete"
        # make sure the user has permission to delete 
        if request.user.is_staff:
            # staff can delete anything 
            Checkout.objects.get(id=id).delete()
            return HttpResponse('DELETED')
        else:
            # not authorized, normal users should be able to cancel 
            # a checkin, but not delete anything 
            return HttpResponse('Not authorized, must be staff, trying cancelling the checkin', status=401)


    return HttpResponse("Method not allowed",status=405)




def task_json(request, id):
    """ Return a particular checkout based on an id in geojson"""
 
    qs = TaskCell.objects.transform(900913).filter(task=id)
    print qs[0].geom
    
    return render_to_response("tasks.json", {"qs" : qs}, mimetype="application/json")


def task_bbox(request,id):
    t = Task.objects.get(id=id)
    return render_to_response("task_bbox.json", {"t": t}, mimetype="application/json")


def tasks_json(request):
    """ Return all the checkouts in geojson """
    # seems like there is a bug where it doesn't transform the geojson string 
    # need to do it manually for now 
    # TODO: this should also return 4326

    qs = Checkout.objects.all().transform(900913)

    for co in qs:
        #print co.geom.geojson
        co.geojson = co.geom.geojson



    return render_to_response("tasks.json", {"qs" : qs}, mimetype="application/json")

def densities_json(request):
    qs = Density.objects.all().transform(900913)

    for d in qs:
        d.geojson = d.geom.geojson

        return render_to_response("densities.json", {"qs": qs}, mimetype="application/json")

    




def checkout(request):
    """ Checkout a bounding box and store it in the database """
    
    # Needs to check if this overlaps with other checkboxes and send 
    # the appropriate error message back
    # Also there is a bug where a request is made with 
    # http://foo.com/api/0.1/checkout?bbox
    # an error occurs 



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


def get_task(request, slug):
    t = Task.objects.get(slug=slug)
    return render_to_response("get_task.html", {'t': t})



    
