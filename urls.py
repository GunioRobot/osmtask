from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^$', 'task.views.index'),

    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^api/0.1/checkout', 'task.views.checkout'),
    (r'^api/0.1/commit', 'task.views.commit'),
    (r'^api/0.1/cancel', 'task.views.cancel'),
    (r'^api/0.1/tasks.json', 'task.views.tasks_json'),
    (r'^api/0.1/densities.json', 'task.views.densities_json'),
    (r'^api/0.1/task/([0-9]+).json', 'task.views.task_json'),
    (r'^api/0.1/task/([0-9]+)$', 'task.views.task'),
    (r'^api/capabilities','osmts.views.capabilities'),
    (r'^osm/$', 'osm.views.index'),
    (r'^osm/1', 'osm.views.showmap'),
    (r'^osm/api/capabilities', 'osm.views.capabilities'),
    (r'^admin/', include(admin.site.urls)),
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': '/Users/tlpinney/project/osmtask/media', 'show_indexes': True}),
                   
)
