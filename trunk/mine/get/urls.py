from django.conf.urls.defaults import *
import views as get
from mine.views import REST

urlpatterns = patterns('',
                       (r'^(?P<key>\w+)$', REST, {'GET': get.read_minekey, 'POST': get.create_minekey}),
                       )
