from django.shortcuts import render
from django.views.generic import ListView
from django.db.models import Sum

from .models import UKLicensedVehicles
from .forms import MostPopularModelsSelectionForm, VehicleSelectionForm


def index(request):
    return render(request, 'vehicles/index.html')


def UKLicensedVehiclesQuery(request):
    year = '2020'

    if request.method == 'POST':
        selection_criteria = VehicleSelectionForm(request.POST)

        if selection_criteria.is_valid():
            if str(selection_criteria.cleaned_data['variant']) != 'None':
                queryset = UKLicensedVehicles.objects.filter(
                    variant__variant=selection_criteria.cleaned_data['variant']).values('year_licensed')\
                    .annotate(total_licensed=Sum('number_licensed'))\
                    .order_by('year_licensed')
            elif str(selection_criteria.cleaned_data['model']) != 'None':
                queryset = UKLicensedVehicles.objects.filter(
                    model__model=selection_criteria.cleaned_data['model']).values('year_licensed')\
                    .annotate(total_licensed=Sum('number_licensed'))\
                    .order_by('year_licensed')
            elif str(selection_criteria.cleaned_data['make']) != 'None':
                queryset = UKLicensedVehicles.objects.filter(
                    make__make=selection_criteria.cleaned_data['make']).values('year_licensed')\
                    .annotate(total_licensed=Sum('number_licensed'))\
                    .order_by('year_licensed')
            errors = None

            context = {'selection_criteria': selection_criteria,
                       'errors': errors,
                       'licensed_vehicles_list': queryset}
            return render(request, 'vehicles/licensed_vehicles_list.html', context)

    else:
        selection_criteria = VehicleSelectionForm()
        errors = selection_criteria.errors or None
        context = {'selection_criteria': selection_criteria, 'errors': errors, }
        return render(request, 'vehicles/licensed_vehicles_list.html', context)


def most_popular_models_list(request):

    if request.method == 'POST':
        selection_criteria = MostPopularModelsSelectionForm(request.POST)

        if selection_criteria.is_valid():
            queryset = UKLicensedVehicles.objects\
                .filter(year_licensed=selection_criteria.cleaned_data['year_licensed'],
                        type__type=selection_criteria.cleaned_data['type'])\
                .values('model__model')\
                .annotate(total_licensed=Sum('number_licensed'))\
                .order_by('-total_licensed')
            errors = None

            context = {'selection_criteria': selection_criteria,
                       'errors': errors,
                       'uklicensedvehicles_list': queryset}
            return render(request, 'vehicles/most_popular_models_list.html', context)

    else:
        selection_criteria = MostPopularModelsSelectionForm()
        errors = selection_criteria.errors or None
        context = {'selection_criteria': selection_criteria, 'errors': errors, }
        return render(request, 'vehicles/most_popular_models_list.html', context)


class MostPopularMakesListView(ListView):
    model = UKLicensedVehicles
    template_name = 'vehicles/most_popular_makes_list.html'
    paginate_by = 50

    def get_queryset(self, **kwargs):
        queryset = UKLicensedVehicles.objects.filter(year_licensed='2020', type__type='Cars')\
            .values('make__make')\
            .annotate(total_licensed=Sum('number_licensed'))\
            .order_by('-total_licensed')
        return queryset
