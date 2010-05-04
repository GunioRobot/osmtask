from django.shortcuts import render_to_response
from django import forms 



class OsmFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()


def capabilities(request):
    """ Return the capabilties of the OpenStreetMap server """
    return render_to_response("osm/capabilities.xml", mimetype="text/xml; charset=utf-8")
    


def showmap(request):
    # right now this is just a stub 
    # testing out how to render OSM data inside of a view 
    # should allow viewing of uploaded osm files 
    return render_to_response("osm/osm.html")


    


def index(request):
    if request.method == 'POST':
        form = OsmFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/osm/success/')
       
    form = OsmFileForm()
            
    return render_to_response("osm.html", { 'form' : form })


