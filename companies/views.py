from django.shortcuts import render
from .forms import *
from mainmenu.views import pagination
# Create your views here.

def index(request):
  return render(request, 'companies/index.html')

def company(request, company_id):
  company = Company.objects.get(id=company_id)
  wiki_categories = CompanyCategory.objects.filter(company=company_id)
  context = {'company': company, 'wiki_categories': wiki_categories}
  return render(request, 'companies/company.html', context)

def companies(request):
    if request.method == 'POST':
        selection_criteria = CompanySelectionForm(request.POST)

        if selection_criteria.is_valid() and selection_criteria.cleaned_data['name'] != None:
            queryset = Company.objects.filter(name__icontains=selection_criteria.cleaned_data['name']).order_by('name')
            errors = None
        else:
            errors = selection_criteria.errors or None
            queryset = Company.objects.order_by('name')
    else:
        selection_criteria = CompanySelectionForm
        errors = selection_criteria.errors or None
        queryset = Company.objects.order_by('name')

    queryset, page = pagination(request, queryset)

    context = {'selection_criteria':selection_criteria, 'errors': errors, 'company_list': queryset, 'page': page}
    return render(request, 'companies/company_list.html', context)

def manufacturer(request, manufacturer_id):
  manufacturer = Manufacturer.objects.get(id=manufacturer_id)
  context = {'manufacturer': manufacturer}
  return render(request, 'companies/manufacturer.html', context)

def manufacturers(request):

    if request.method == 'POST':
        selection_criteria = ManufacturerSelectionForm(request.POST)

        if selection_criteria.is_valid() and selection_criteria.cleaned_data['name'] != None:
            queryset = Manufacturer.objects.filter(name__icontains=selection_criteria.cleaned_data['name']).order_by('name')
            errors = None
        else:
            errors = selection_criteria.errors or None
            queryset = Manufacturer.objects.order_by('name')
    else:
        selection_criteria = ManufacturerSelectionForm()
        errors = selection_criteria.errors or None
        queryset = Manufacturer.objects.order_by('name')

    queryset, page = pagination(request, queryset)

    context = {'selection_criteria':selection_criteria, 'errors': errors, 'manufacturer_list': queryset, 'page': page}
    return render(request, 'companies/manufacturer_list.html', context)