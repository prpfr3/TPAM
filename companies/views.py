from django.shortcuts import render, redirect
from django.http import QueryDict
from django.db.models import Q
from .forms import *

from mainmenu.views import pagination


def index(request):
    return render(request, "companies/index.html")


def companies(request):
    errors = None
    items_per_page = 30

    # Load selection criteria from session if available, fallback to form data otherwise
    if request.method == "POST":
        selection_criteria = CompanySelectionForm(request.POST)
        if selection_criteria.is_valid():
            # Save criteria to session
            request.session["selection_criteria"] = request.POST.dict()
            return redirect(request.path_info)
    else:
        # Initialize form with session-stored data or empty
        form_data = request.session.get("selection_criteria", None)
        selection_criteria = CompanySelectionForm(form_data)

    # Default to all records if no valid selection criteria
    queryset = Company.objects.all().order_by("name")

    if not selection_criteria.is_valid():
        errors = selection_criteria.errors
    else:
        query = Q()
        name_query = selection_criteria.cleaned_data.get("name", "")
        if name_query:
            query &= Q(name__icontains=name_query)
        queryset = Company.objects.filter(query).order_by("name")

    queryset = pagination(request, queryset, items_per_page)

    context = {
        "selection_criteria": selection_criteria,
        "errors": errors,
        "queryset": queryset,
    }
    return render(request, "companies/companies.html", context)


def company(request, company_id):
    import wikipediaapi, urllib
    from locations.models import Route

    company = Company.objects.get(id=company_id)
    predecessor_companies = Company.objects.filter(successor_company=company_id)
    wiki_categories = CompanyCategory.objects.filter(company=company_id)
    routes = Route.objects.filter(owneroperators=company).order_by("name")
    posts = company.posts.all()
    if company.wikislug:
        wikipediaapi.log.setLevel(level=wikipediaapi.logging.DEBUG)
        wiki_wiki = wikipediaapi.Wikipedia(
            user_agent="github/prpfr3 TPAM",
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
        "posts": posts,
        "wiki_categories": wiki_categories,
        "description_type": description_type,
        "description": description,
        "routes": routes,
        "predecessor_companies": predecessor_companies,
    }
    return render(request, "companies/company.html", context)


def manufacturers(request):
    errors = None
    items_per_page = 30

    # Load selection criteria from session if available, or use empty data on first load
    if request.method == "POST":
        selection_criteria = ManufacturerSelectionForm(request.POST)
        if selection_criteria.is_valid():
            # Save criteria to session
            request.session["manufacturer_selection_criteria"] = request.POST.dict()
            return redirect(request.path_info)
    else:
        # Initialize form with session-stored data or empty if none available
        form_data = request.session.get("manufacturer_selection_criteria", None)
        selection_criteria = ManufacturerSelectionForm(form_data)

    # Default to all records if no valid selection criteria
    queryset = Manufacturer.objects.all().order_by("name")

    if selection_criteria.is_valid():
        query = Q()
        name_query = selection_criteria.cleaned_data.get("name", "")
        if name_query:
            query &= Q(name__icontains=name_query)
        queryset = Manufacturer.objects.filter(query).order_by("name")
    else:
        errors = selection_criteria.errors

    queryset = pagination(request, queryset, items_per_page)

    context = {
        "selection_criteria": selection_criteria,
        "errors": errors,
        "queryset": queryset,
    }
    return render(request, "companies/manufacturers.html", context)


def manufacturer(request, manufacturer_id):
    manufacturer = Manufacturer.objects.get(id=manufacturer_id)
    context = {"manufacturer": manufacturer}
    return render(request, "companies/manufacturer.html", context)
