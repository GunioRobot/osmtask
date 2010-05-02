from django.shortcuts import render_to_response 



def capabilities(request):
    """ Return the capabilties of the OSM Task Server """
    return render_to_response("osmts/capabilities.xml", mimetype="text/xml; charset=utf-8")




