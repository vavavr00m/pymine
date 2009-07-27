# Create your views here.
#
#from django.http import HttpResponse
#
#def index(request):
#    return HttpResponse("Hello, world. This is the frontend index.")
#
#def detail(request, poll_id):
#    return HttpResponse("You're looking at poll %s." % poll_id)
#------------------------------------------------------------------
#
#from django.template import Context, loader
#from mysite.polls.models import Poll
#from django.http import HttpResponse
#
#def index(request):
#    latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
#    t = loader.get_template('polls/index.html')
#    c = Context({
#        'latest_poll_list': latest_poll_list,
#    })
#    return HttpResponse(t.render(c))
#
#
#------------------------------------------------------------------
#def index(request):
#    latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
#    return render_to_response('polls/index.html', {'latest_poll_list': latest_poll_list})


from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404

import datetime

def root(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)

def rest():
    get_view = kwargs.pop('GET', None)
    post_view = kwargs.pop('POST', None)
    put_view = kwargs.pop('PUT', None)
    delete_view = kwargs.pop('DELETE', None)

    if request.method == 'GET' and get_view is not None:
        return get_view(request, *args, **kwargs)

    elif request.method == 'POST' and post_view is not None:
        return post_view(request, *args, **kwargs)

    elif request.method == 'PUT' and put_view is not None:
        return put_view(request, *args, **kwargs)

    elif request.method == 'DELETE' and delete_view is not None:
        return delete_view(request, *args, **kwargs)

    raise Http404
