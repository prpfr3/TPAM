from itertools import chain

import wikipediaapi
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.http import QueryDict
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from notes.models import Reference
from mainmenu.views import pagination
from .forms import *
from .models import *


def index(request):
    return render(request, "locos/index.html")


def loco_classes(request):
    errors = None
    page = None

    queryset = LocoClass.objects.order_by("wikiname")
    selection_criteria = LocoClassSelectionForm(request.GET or None)

    # This code changes the POST into GET which is a method of retaining the form selections
    if request.method == "POST":
        return redirect(request.path_info + "?" + request.POST.urlencode())

    if not selection_criteria.is_valid():
        errors = selection_criteria.errors

    if selection_criteria.is_valid():
        queryset = loco_classes_query_build(selection_criteria.cleaned_data)

    queryset, page = pagination(request, queryset)

    # Retain existing query parameters for pagination
    query_params = QueryDict("", mutable=True)
    query_params.update(request.GET)

    context = {
        "selection_criteria": selection_criteria,
        "errors": errors,
        "queryset": queryset,
        "query_params": query_params.urlencode(),
    }
    return render(request, "locos/loco_class_list.html", context)


def loco_classes_query_build(selection_criteria):

    conditions = Q()
    cleandata = selection_criteria

    if "name" in cleandata and cleandata["name"]:
        fk_ids = [fk.lococlass_fk_id for fk in cleandata["name"]]
        conditions &= Q(id__in=fk_ids)

    if "wikiname" in cleandata and cleandata["wikiname"]:
        conditions &= Q(wikiname__icontains=cleandata["wikiname"])

    if "wheel_body_type" in cleandata and cleandata["wheel_body_type"]:
        conditions &= Q(wheel_body_type__icontains=cleandata["wheel_body_type"])

    if "wheel_arrangement" in cleandata and cleandata["wheel_arrangement"]:
        conditions &= Q(wheel_arrangement__icontains=cleandata["wheel_arrangement"])

    if "designer_person" in cleandata and cleandata["designer_person"]:
        fk = cleandata["designer_person"]
        conditions &= Q(designer_person_id=fk)

    if "owner_operators" in cleandata and cleandata["owner_operators"]:
        fk = cleandata["owner_operators"]
        conditions &= Q(owner_operators=fk)

    if "manufacturers" in cleandata and cleandata["manufacturers"]:
        fk = cleandata["manufacturers"]
        conditions &= Q(manufacturers=fk)

    queryset = LocoClass.objects.filter(conditions).order_by("wikiname")

    return queryset


def loco_class(request, slug):

    loco_class = LocoClass.objects.filter(slug=slug).order_by("wikiname").first()

    locomotives = Locomotive.objects.filter(lococlass=loco_class.id)
    references = loco_class.references.all()
    operators = loco_class.owner_operators.all()
    manufacturers = loco_class.manufacturers.all()

    context = {
        "loco_class": loco_class,
        "locomotives": locomotives,
        "operators": operators,
        "references": references,
        "manufacturers": manufacturers,
    }

    return render(request, "locos/loco_class.html", context)


def locomotives(request):
    errors = None
    queryset = Locomotive.objects.order_by("name")
    selection_criteria = LocomotiveSelectionForm(request.GET or None)

    if request.method == "POST":
        # Use GET method for form submission
        return redirect(request.path_info + "?" + request.POST.urlencode())

    if not selection_criteria.is_valid():
        errors = selection_criteria.errors

    if selection_criteria.is_valid() and selection_criteria.cleaned_data["identifier"]:
        queryset = (
            Locomotive.objects.filter(
                identifier__icontains=selection_criteria.cleaned_data.get(
                    "identifier", ""
                )
            )
            .values("brd_class_name")
            .annotate(total=Count("brd_class_name"))
            .order_by("total")
        )

    queryset, page = pagination(request, queryset)

    # Retain existing query parameters for pagination
    query_params = QueryDict("", mutable=True)
    query_params.update(request.GET)

    context = {
        "selection_criteria": selection_criteria,
        "errors": errors,
        "queryset": queryset,
        "query_params": query_params.urlencode(),
    }
    return render(request, "locos/locomotives_list.html", context)


def locomotive(request, locomotive_id):
    lococlass = None
    operators = None
    class_designers = None
    class_designers2 = None
    class_designers3 = None
    class_manufacturers = None
    class_manufacturers2 = None
    class_manufacturers3 = None
    locomotive = Locomotive.objects.get(id=locomotive_id)
    try:
        lococlass = LocoClass.objects.get(id=locomotive.lococlass)
    except ObjectDoesNotExist:
        pass
    except Exception as e:
        print(f"{e=}")
    else:
        operators = lococlass.company_owneroperator.all()
        class_designers1 = lococlass.location_event_designer.all()
        class_designers2 = lococlass.manufacturer_designer.all()
        class_designers3 = lococlass.company_designer.all()

        class_designers = list(
            chain(class_designers1, class_designers2, class_designers3)
        )

        class_manufacturers1 = lococlass.location_event_manufacturer.all()
        class_manufacturers2 = lococlass.manufacturer_manufacturer.all()
        class_manufacturers3 = lococlass.company_manufacturer.all()

        class_manufacturers = list(
            chain(class_manufacturers1, class_manufacturers2, class_manufacturers3)
        )

    # references = Reference.objects.filter(loco=locomotive_id)

    wiki_wiki = wikipediaapi.Wikipedia(
        user_agent="github/prpfr3 TPAM",
        language="en",
        extract_format=wikipediaapi.ExtractFormat.HTML,
    )
    # The following could be introduced at a later date for where there is a Wikipedia page for a locomotive
    # page_name = locomotive.wikipedia_name.replace(' ', '_')
    # wikipedia_summary = wiki_wiki.page(page_name).text

    context = {
        "locomotive": locomotive,
        "lococlass": lococlass,
        "operators": operators,
        # 'references':references,
        "designers": class_designers,
        "manufacturers": class_manufacturers,
        # 'wikipedia_summary':wikipedia_summary,
    }

    return render(request, "locos/locomotive.html", context)


def photos(request):
    queryset = Reference.objects.filter(type="6").order_by("full_reference")

    paginator = Paginator(queryset, 40)
    page = request.GET.get("page")

    # Retain existing query parameters for pagination links

    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver the last page of results
        paginated_queryset = paginator.page(paginator.num_pages)

    context = {"page": page, "photos": paginated_queryset}
    print(context)
    return render(request, "locos/photos.html", context)


def photos(request):
    errors = None
    queryset = Reference.objects.filter(type="6").order_by("full_reference")
    selection_criteria = LocomotiveImageForm(request.GET or None)

    if selection_criteria.is_valid():
        queryset = photos_query_build(selection_criteria.cleaned_data)

    # This code changes the POST into GET which is a method of retaining the form selections
    if request.method == "POST":
        return redirect(request.path_info + "?" + request.POST.urlencode())

    if not selection_criteria.is_valid():
        errors = selection_criteria.errors

    queryset, page = pagination(request, queryset)

    # Retain existing query parameters for pagination
    query_params = QueryDict("", mutable=True)
    query_params.update(request.GET)

    context = {
        "selection_criteria": selection_criteria,
        "errors": errors,
        "queryset": queryset,
        "query_params": query_params.urlencode(),
    }

    return render(request, "locos/photos.html", context)


def photos_query_build(selection_criteria):

    conditions = Q()
    cleandata = selection_criteria

    if "full_reference" in cleandata and cleandata["full_reference"]:
        conditions &= Q(full_reference__icontains=cleandata["full_reference"])

    conditions &= Q(type="6")

    queryset = Reference.objects.filter(conditions).order_by("full_reference")

    return queryset


def photo(request, photo_id):
    photo = Reference.objects.get(id=photo_id)
    loco_classes = photo.lococlass_set.all()
    locations = photo.location_set.all()
    context = {"photo": photo, "classes": loco_classes, "locations": locations}
    return render(request, "locos/photo.html", context)
