from django.shortcuts import render, redirect
from django.http import QueryDict
from .forms import *

from mainmenu.views import pagination

# Create your views here.


def index(request):
    return render(request, "companies/index.html")


def companies(request):
    errors = None
    queryset = Manufacturer.objects.order_by("name")
    selection_criteria = ManufacturerSelectionForm(request.POST)

    if request.method == "POST":
        # Use GET method for form submission
        return redirect(request.path_info + "?" + request.POST.urlencode())

    if not selection_criteria.is_valid():
        errors = selection_criteria.errors

    if (
        selection_criteria.is_valid()
        and selection_criteria.cleaned_data["name"] != None
    ):
        queryset = Manufacturer.objects.filter(
            name__icontains=selection_criteria.cleaned_data["name"]
        ).order_by("name")

    queryset, page = pagination(request, queryset)

    # Retain existing query parameters for pagination
    query_params = QueryDict("", mutable=True)
    query_params.update(request.GET)

    context = {
        "selection_criteria": selection_criteria,
        "errors": errors,
        "queryset": queryset,
        "page": page,
    }
    return render(request, "companies/companies.html", context)


def company(request, company_id):
    import wikipediaapi, urllib
    from locations.models import Route

    company = Company.objects.get(id=company_id)
    predecessor_companies = Company.objects.filter(successor_company=company_id)
    wiki_categories = CompanyCategory.objects.filter(company=company_id)
    routes = Route.objects.filter(owneroperators=company).order_by("name")

    # # Get either a customised post or otherwise a wikipedia page
    if company.post_fk:
        description = company.post_fk.body
        description_type = "Notes"
    elif company.wikislug:
        import sys

        wikipediaapi.log.setLevel(level=wikipediaapi.logging.DEBUG)
        wiki_wiki = wikipediaapi.Wikipedia(
            # user_agent="github/prpfr3 TPAM",
            language="en",
            extract_format=wikipediaapi.ExtractFormat.HTML,
        )
        slug = company.wikislug.replace("/wiki/", "")
        slug = urllib.parse.unquote(slug, encoding="utf-8", errors="replace")
        page_html = wiki_wiki.page(slug)
        description = page_html.text
        description_type = "From Wikipedia:-"
    else:
        description = None
        description_type = None

    context = {
        "company": company,
        "wiki_categories": wiki_categories,
        "description_type": description_type,
        "description": description,
        "routes": routes,
        "predecessor_companies": predecessor_companies,
    }
    return render(request, "companies/company.html", context)


def manufacturers(request):
    errors = None
    queryset = Manufacturer.objects.order_by("name")
    selection_criteria = ManufacturerSelectionForm(request.POST)

    if request.method == "POST":
        # Use GET method for form submission
        return redirect(request.path_info + "?" + request.POST.urlencode())

    if not selection_criteria.is_valid():
        errors = selection_criteria.errors

    if (
        selection_criteria.is_valid()
        and selection_criteria.cleaned_data["name"] != None
    ):
        queryset = Manufacturer.objects.filter(
            name__icontains=selection_criteria.cleaned_data["name"]
        ).order_by("name")

    queryset, page = pagination(request, queryset)

    # Retain existing query parameters for pagination
    query_params = QueryDict("", mutable=True)
    query_params.update(request.GET)

    context = {
        "selection_criteria": selection_criteria,
        "errors": errors,
        "queryset": queryset,
        "page": page,
    }
    return render(request, "companies/manufacturers.html", context)


def manufacturer(request, manufacturer_id):
    manufacturer = Manufacturer.objects.get(id=manufacturer_id)
    context = {"manufacturer": manufacturer}
    return render(request, "companies/manufacturer.html", context)
