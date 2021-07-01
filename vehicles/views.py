from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView

from .models import UKLicensedVehicles
from .forms import VehicleSelectionForm

def index(request):
  return render(request, 'vehicles/index.html')

class UKLicensedVehiclesListView(ListView):
    model = UKLicensedVehicles
    paginate_by = 50
#    template_name = <app_label>/<model>_list.html by default
#    context_object_name = <model>_list by default
#    queryset = <model>.objects.all() by default

    def get_queryset(self, **kwargs):
        s_variant = self.kwargs['variant']
        queryset = UKLicensedVehicles.objects.filter(
            variant__variant=self.kwargs['variant'],
            #make__make=self.kwargs['make'],
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = self.kwargs['type']
        context['make'] = self.kwargs['make']
        context['model'] = self.kwargs['model']
        context['variant'] = self.kwargs['variant']
        return context


def choose_vehicle(request):

    if request.method == 'POST':
        selection_criteria = VehicleSelectionForm(request.POST)

        if selection_criteria.is_valid():
            s_type = str(selection_criteria.cleaned_data['type'])
            s_make = str(selection_criteria.cleaned_data['make'])
            s_model = str(selection_criteria.cleaned_data['model'])
            s_variant = str(selection_criteria.cleaned_data['variant'])
            return HttpResponseRedirect(reverse('vehicles:UK_licensed_vehicles', args=[s_type, s_make, s_model, s_variant]))

    else:
        selection_criteria = VehicleSelectionForm()
        errors = selection_criteria.errors or None
        context = {'selection_criteria':selection_criteria, 'errors': errors,}
        return render(request, 'vehicles/choose_vehicle.html', context)