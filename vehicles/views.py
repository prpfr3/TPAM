from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.db.models import Count, Sum

from .models import UKLicensedVehicles
from .forms import MostPopularModelsSelectionForm, VehicleSelectionForm
def index(request):
  return render(request, 'vehicles/index.html')

class UKLicensedVehiclesListView(ListView):
    model = UKLicensedVehicles
    paginate_by = 50
#    template_name = <app_label>/<model>_list.html by default
#    context_object_name = <model>_list by default
#    queryset = <model>.objects.all() by default

    def get_queryset(self, **kwargs):
        if self.kwargs['variant'] != 'None':
            queryset = UKLicensedVehicles.objects.filter(
                variant__variant=self.kwargs['variant']).values('year_licensed')\
                    .annotate(total_licensed=Sum('number_licensed'))\
                    .order_by('year_licensed')
        elif self.kwargs['model'] != 'None':
            queryset = UKLicensedVehicles.objects.filter(
                model__model=self.kwargs['model']).values('year_licensed')\
                    .annotate(total_licensed=Sum('number_licensed'))\
                    .order_by('year_licensed')
        else:
            queryset = UKLicensedVehicles.objects.filter(
                make__make=self.kwargs['make']).values('year_licensed')\
                    .annotate(total_licensed=Sum('number_licensed'))\
                    .order_by('year_licensed')      
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = self.kwargs['type']
        context['make'] = self.kwargs['make']
        context['model'] = self.kwargs['model']
        context['variant'] = self.kwargs['variant']
        return context

class MostPopularModelsListView(ListView):
    model = UKLicensedVehicles
    template_name = 'vehicles/mostpopularmodels_list.html'
    paginate_by = 50

    def get_queryset(self, **kwargs):
        queryset = UKLicensedVehicles.objects\
                .filter(year_licensed=self.kwargs['year'], type__type=self.kwargs['type'])\
                .values('model__model')\
                .annotate(total_licensed=Sum('number_licensed'))\
                .order_by('-total_licensed')
        print(f'{queryset=}')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['year_licensed'] = self.kwargs['year']
        context['type'] = self.kwargs['type']
        return context

class MostPopularMakesListView(ListView):
    model = UKLicensedVehicles
    template_name = 'vehicles/mostpopularmakes_list.html'
    paginate_by = 50

    def get_queryset(self, **kwargs):
        queryset = UKLicensedVehicles.objects.filter(year_licensed='2019', type__type='Cars')\
                .values('make__make')\
                .annotate(total_licensed=Sum('number_licensed'))\
                .order_by('-total_licensed')
        print(f'{queryset=}')
        return queryset

def choose_vehicle(request):

    if request.method == 'POST':
        selection_criteria = VehicleSelectionForm(request.POST)

        if selection_criteria.is_valid():
            s_type = str(selection_criteria.cleaned_data['type'])
            s_make = str(selection_criteria.cleaned_data['make'])
            s_model = str(selection_criteria.cleaned_data['model'])
            s_variant = str(selection_criteria.cleaned_data['variant'])
            print(f'{s_model=}', f'{s_variant=}')
            return HttpResponseRedirect(reverse('vehicles:UK_licensed_vehicles', args=[s_type, s_make, s_model, s_variant]))

    else:
        selection_criteria = VehicleSelectionForm()
        errors = selection_criteria.errors or None
        context = {'selection_criteria':selection_criteria, 'errors': errors,}
        return render(request, 'vehicles/choose_vehicle.html', context)

def most_popular_models_selection(request):

    if request.method == 'POST':
        selection_criteria = MostPopularModelsSelectionForm(request.POST)

        if selection_criteria.is_valid():
            s_type = str(selection_criteria.cleaned_data['type'])
            s_year = str(selection_criteria.cleaned_data['year_licensed'])
            print(f'{s_type=}', f'{s_year=}')
            return HttpResponseRedirect(reverse('vehicles:most_popular_models', args=[s_type, s_year]))

    else:
        selection_criteria = MostPopularModelsSelectionForm()
        errors = selection_criteria.errors or None
        context = {'selection_criteria':selection_criteria, 'errors': errors,}
        return render(request, 'vehicles/most_popular_models_selection.html', context)