from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import NaPTANRailReferences
from .forms import GetLocationForm, ChooseLocationForm 

from .opentransport_api import otapi_timetable, otapi_location, otapi_livepassenger, otapi_livefreight, otapi_service

def index(request):
  return render(request, 'rtt/index.html')

def chooselocation(request):
  if request.method == 'POST':
      selection_criteria = ChooseLocationForm(request.POST)
      if selection_criteria.is_valid():     
          errors = None
          print(selection_criteria.cleaned_data['crscode'])            
          context = {'selection_criteria': selection_criteria, 
                      'errors': errors, 
                      'livefreight': otapi_livefreight(selection_criteria.cleaned_data['crscode'])}
          return render(request, 'rtt/getlivefreight2.html', context)
  else:
      locations = NaPTANRailReferences.objects.order_by('crscode')
      selection_criteria = ChooseLocationForm()
      errors = selection_criteria.errors or None
      context = {'selection_criteria':selection_criteria, 'locations': locations, 'errors': errors,}
      return render(request, 'rtt/getlivefreight2.html', context)

def gettimes(request, crscode):
  context = {'departures': otapi_timetable(crscode)}
  return render(request, 'rtt/gettimes.html', context)

def getlivepassenger(request, crscode):
  context = {'livepassenger': otapi_livepassenger(crscode)}
  return render(request, 'rtt/getlivepassenger.html', context)

def getlivefreight(request, crscode):
  context = {'livefreight': otapi_livefreight(crscode)}
  return render(request, 'rtt/getlivefreight.html', context)

def getlivefreight2(request, crscode):
  context = {'livefreight': otapi_livefreight(crscode)}
  return render(request, 'rtt/getlivefreight2.html', context)

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