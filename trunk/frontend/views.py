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

from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404
from mysite.polls.models import Poll

def index(request):
    latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
    return render_to_response('polls/index.html', {'latest_poll_list': latest_poll_list})


