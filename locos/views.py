from itertools import chain

import wikipediaapi
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, ExpressionWrapper, F, fields
from django.http import HttpRequest, HttpResponseRedirect, QueryDict
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from .forms import *
from .models import *
from notes.models import Reference
from mainmenu.views import pagination


def index(request):
    return render(request, "locos/index.html")


def loco_class(request, loco_class_id):
    loco_class = LocoClass.objects.get(id=loco_class_id)
    context = {"loco_class": loco_class}
    return render(request, "locos/loco_class.html", context)


def loco_classes(request):
    errors = None
    queryset = LocoClass.objects.order_by("wikiname")
    selection_criteria = LocoClassSelectionForm(request.GET or None)

    if request.method == "POST":
        # Use GET method for form submission
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
    import urllib
    from django.db.models import F, Value
    from django.db.models.functions import Replace

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

    queryset = (
        LocoClass.objects.filter(conditions)
        # .annotate(wikislug=Replace(F("slug"), Value(" "), Value("_")))
        .order_by("wikiname")
    )

    # Fetch the queryset and then decode the URLs
    # for obj in queryset:
    #     obj.wikislug = urllib.parse.unquote(
    #         obj.wikislug, encoding="utf-8", errors="replace"
    #     )

    return queryset


def loco_class(request, slug):
    import urllib
    from django.db.models import F, Value
    from django.db.models.functions import Concat, Replace

    loco_class = (
        LocoClass.objects.filter(slug=slug)
        # .annotate(wikislug=Replace(F("slug"), Value(" "), Value("_")))
        .order_by("wikiname").first()  # Retrieve the first object from the queryset
    )
    # loco_class.wikislug = urllib.parse.unquote(
    #     loco_class.wikislug, encoding="utf-8", errors="replace"
    # )

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

    if selection_criteria.is_valid():
        if selection_criteria.cleaned_data["identifier"]:
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
        language="en", extract_format=wikipediaapi.ExtractFormat.HTML
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
    photos = Reference.objects.filter(type="6").order_by("full_reference")
    paginator = Paginator(photos, 33)
    page = request.GET.get("page")
    try:
        photos = paginator.page(page)
    except PageNotAnInteger:
        photos = paginator.page(1)
    except EmptyPage:
        photos = paginator.page(paginator.num_pages)
    context = {"page": page, "photos": photos}
    return render(request, "locos/photos.html", context)


def photo(request, photo_id):
    photo = Reference.objects.get(id=photo_id)
    loco_classes = photo.lococlass_set.all()
    locations = photo.location_set.all()
    context = {"photo": photo, "classes": loco_classes, "locations": locations}
    return render(request, "locos/photo.html", context)
