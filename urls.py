from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^$', 'task.views.index'),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^api/0.1/checkout', 'task.views.checkout'),
    (r'^api/0.1/commit', 'task.views.commit'),
    (r'^api/0.1/cancel', 'task.views.cancel'),
    (r'^api/0.1/tasks.json', 'task.views.tasks_json'),
    (r'^admin/', include(admin.site.urls)),
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': '/Users/tlpinney/project/osmtask/media', 'show_indexes': True}),
                   
)
