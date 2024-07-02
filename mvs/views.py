import contextlib

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.utils import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from mainmenu.views import pagination

from .forms import *
from .models import *


def index(request):
    return render(request, "mvs/index.html")


def MVBMimage_create(request):
    if request.method == "POST":
        form = MVBMImageCreateForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_item = form.save(commit=False)
            new_item.user = request.user
            new_item.save()
            messages.success(request, "Image added successfully")
            return redirect(new_item.get_absolute_url())
    else:
        form = MVBMImageCreateForm(data=request.GET)
        context = {"section": "images", "form": form}
        return render(request, "mvs/mvbmimage_new.html", context)


def military_vehicle_classes(request):

    errors = None
    favorites = []

    if request.method == "POST":
        selection_criteria = MilitaryVehicleClassSelectionForm(request.POST)

        if (
            selection_criteria.is_valid()
            and selection_criteria.cleaned_data["mvclass"] != None
        ):
            queryset = MilitaryVehicleClass.objects.filter(
                mvclass__icontains=selection_criteria.cleaned_data["mvclass"]
            ).order_by("mvclass")
            if request.user.is_authenticated:
                rows = request.user.favorite_things.values("id")
                favorites = [row["id"] for row in rows]
        else:
            errors = selection_criteria.errors or None
            queryset = MilitaryVehicleClass.objects.order_by("mvclass")
    else:
        selection_criteria = MilitaryVehicleClassSelectionForm()
        queryset = MilitaryVehicleClass.objects.order_by("mvclass")

    context = {
        "selection_criteria": selection_criteria,
        "errors": errors,
        "favorites": favorites,
        "military_vehicle_classes": queryset,
    }
    return render(request, "mvs/military_vehicle_class_list.html", context)


# csrf exemption in class based views
# https://stackoverflow.com/questions/16458166/how-to-disable-djangos-csrf-validation


@method_decorator(csrf_exempt, name="dispatch")
class AddFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        t = get_object_or_404(MilitaryVehicleClass, id=pk)
        fav = Fav(user=request.user, thing=t)
        with contextlib.suppress(IntegrityError):
            fav.save()  # In case of duplicate key
        return HttpResponse()


@method_decorator(csrf_exempt, name="dispatch")
class DeleteFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        t = get_object_or_404(MilitaryVehicleClass, id=pk)
        with contextlib.suppress(Fav.DoesNotExist):
            fav = Fav.objects.get(user=request.user, thing=t).delete()
        return HttpResponse()


def military_vehicle_class(request, military_vehicle_class_id):
    military_vehicle_class = MilitaryVehicleClass.objects.get(
        id=military_vehicle_class_id
    )
    context = {"military_vehicle_class": military_vehicle_class}
    return render(request, "mvs/military_vehicle_class.html", context)


def locations(request):
    locations = HeritageSite.objects.order_by("site_name")
    paginator = Paginator(locations, 33)
    page = request.GET.get("page")
    try:
        locations = paginator.page(page)
    except PageNotAnInteger:
        locations = paginator.page(1)
    except EmptyPage:
        locations = paginator.page(paginator.num_pages)
    context = {"page": page, "locations": locations}
    return render(request, "mvs/locations.html", context)


def photos(request):
    photos = MVImage.objects.order_by("image_name")
    photos, page = pagination(request, photos, 36)
    context = {"page": page, "queryset": photos}
    return render(request, "mvs/photos.html", context)


def photo(request, mvimage_id):
    photo = MVImage.objects.get(id=mvimage_id)
    context = {"photo": photo}
    return render(request, "mvs/photo.html", context)


@login_required
def new_photo(request):
    if request.method != "POST":
        form = MVImageForm()
    else:
        form = MVImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("mvs:photos"))

    context = {"form": form}
    return render(request, "mvs/photo_new.html", context)


@login_required
def edit_photo(request, mvimage_id):
    photo = MVImage.objects.get(id=mvimage_id)

    if request.method != "POST":
        form = MVImageForm(instance=photo)
    else:
        form = MVImageForm(instance=photo, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("mvs:photo", args=[mvimage_id]))

    context = {"photo": photo, "form": form}
    return render(request, "mvs/photo_edit.html", context)
