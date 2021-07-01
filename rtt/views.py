from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import NaPTANRailReferences
from .forms import GetLocationForm 

from .opentransport_api import otapi_timetable, otapi_location, otapi_livepassenger, otapi_livefreight, otapi_service

def index(request):
  return render(request, 'rtt/index.html')

def gettimes(request, crscode):
  context = {'departures': otapi_timetable(crscode)}
  return render(request, 'rtt/gettimes.html', context)

def getlivepassenger(request, crscode):
  context = {'livepassenger': otapi_livepassenger(crscode)}
  return render(request, 'rtt/getlivepassenger.html', context)

def getlivefreight(request, crscode):
  context = {'livefreight': otapi_livefreight(crscode)}
  return render(request, 'rtt/getlivefreight.html', context)

def getservice(request, uid):
  context = {'service': otapi_service(uid)}
  return render(request, 'rtt/getservice.html', context)

def getlocations(request):
  locations = NaPTANRailReferences.objects.order_by('crscode')
  context = {'locations': locations}
  return render(request, 'rtt/getlocations.html', context)

#def getlocation(request, location_id):
#  location = NaPTANRailReferences.objects.get(id=location_id)
#  context = {'location': location}
#  return render(request, 'rtt/getlocation.html', context)

def getlocation(request, location_id):
  location = NaPTANRailReferences.objects.get(id=location_id)
  if request.method != 'POST': 
    form = GetLocationForm(instance=location)
    context = {'location': location,'form': form} 
    return render(request, 'rtt/getlocation.html', context)
  else:
    form = GetLocationForm(instance=location, data=request.POST)
    if form.is_valid():
      return HttpResponseRedirect(reverse('rtt:gettimes', args=[location_id]))