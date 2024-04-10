from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import NaPTANRailReferences
from .forms import LocationForm

from .opentransport_api import (
    otapi_timetable,
    otapi_location,
    otapi_livepassenger,
    otapi_livefreight,
    otapi_service,
)


def index(request):
    return render(request, "rtt/index.html")


def locations(request):
    locations = NaPTANRailReferences.objects.order_by("crscode")
    context = {"locations": locations}
    return render(request, "rtt/locations.html", context)


# def location(request, location_id):
# location = NaPTANRailReferences.objects.(id=location_id)
def location(request, crscode):
    location = NaPTANRailReferences.objects.get(crscode=crscode)
    if request.method != "POST":
        form = LocationForm(instance=location)
        context = {"location": location, "form": form}
        return render(request, "rtt/location.html", context)
    else:
        form = LocationForm(instance=location, data=request.POST)
        if form.is_valid():
            # return HttpResponseRedirect(reverse('rtt:times', args=[location_id]))
            return HttpResponseRedirect(reverse("rtt:times", args=[crscode]))


def livefreight(request, crscode):
    context = {"livefreight": otapi_livefreight(crscode)}
    return render(request, "rtt/livefreight.html", context)


def livepassenger(request, crscode):
    context = {"livepassenger": otapi_livepassenger(crscode)}
    return render(request, "rtt/livepassenger.html", context)


def service(request, uid):
    context = {"service": otapi_service(uid)}
    return render(request, "rtt/service.html", context)


def times(request, crscode):
    context = {"departures": otapi_timetable(crscode)}
    return render(request, "rtt/times.html", context)
