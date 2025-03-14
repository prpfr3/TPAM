import configparser
import os

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core import serializers
from django.core.mail import send_mail
from django.db.models import Q
from django.http import QueryDict
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from mainmenu.models import Profile
from mainmenu.views import pagination
from django.db.models import F, Func, Value, CharField
from django.db.models.functions import Concat, Substr, Cast
from cart.forms import CartAddProductForm

from .forms import *
from .models import *

"""
# Explanatory notes for the Owner views

 https://docs.djangoproject.com/en/3.0/ref/class-based-views/mixins-editing/#django.views.generic.edit.ModelFormMixin.form_valid

 https://stackoverflow.com/questions/862522/django-populate-user-id-when-saving-a-model

 https://stackoverflow.com/a/15540149

 https://stackoverflow.com/questions/5531258/example-of-django-class-based-deleteview
"""


class OwnerListView(ListView):
    """
    Sub-class the ListView to pass the request to the form.
    """


class OwnerDetailView(DetailView):
    """
    Sub-class the DetailView to pass the request to the form.
    """


class OwnerCreateView(LoginRequiredMixin, CreateView):
    """
    Sub-class of the CreateView to automatically pass the Request to the Form
    and add the owner to the saved object.
    """

    # Saves the form instance, sets the current object for the view, and redirects to get_success_url().
    def form_valid(self, form):  # sourcery skip: avoid-builtin-shadow
        object = form.save(commit=False)
        object.owner = get_object_or_404(Profile, user=self.request.user)
        object.save()
        return super(OwnerCreateView, self).form_valid(form)


class OwnerUpdateView(LoginRequiredMixin, UpdateView):
    """
    Sub-class the UpdateView to pass the request to the form and limit the
    queryset to the requesting user.
    """

    # def get_queryset(self):
    #     """Limit a User to only modifying their own data."""
    #     qs = super(OwnerUpdateView, self).get_queryset()

    #     return qs.filter(owner=get_object_or_404(Profile, user=self.request.user))

    def get_queryset(self):
        """Limit a User to only modifying their own data."""
        qs = super(OwnerUpdateView, self).get_queryset()

        # Get the User instance from the Profile
        user = get_object_or_404(Profile, user=self.request.user).user

        return qs.filter(owner=user)


class OwnerDeleteView(LoginRequiredMixin, DeleteView):
    """
    Sub-class the DeleteView to restrict a User from deleting other
    user's data.
    """

    def get_queryset(self):
        qs = super(OwnerDeleteView, self).get_queryset()
        # Get the User instance from the Profile
        user = get_object_or_404(Profile, user=self.request.user).user

        return qs.filter(owner=user)


def index(request):
    return render(request, "notes/index.html")


class TopicListView(OwnerListView):
    model = Topic


class PostListView(OwnerListView):
    model = Post
    ordering = ["title"]


class TopicDetailView(OwnerDetailView):
    model = Topic

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["posts"] = context["topic"].post_set.all()

        if strval := self.request.GET.get("search", False):
            query = Q(title__icontains=strval)
            query.add(Q(body__icontains=strval), Q.OR)
            post_list = (
                Post.objects.filter(query).select_related().order_by("-updated")[:10]
            )
            context["posts"] = (
                context["topic"]
                .post_set.filter(query)
                .select_related()
                .order_by("-updated")[:10]
            )
        else:
            context["posts"] = context["topic"].post_set.all()
        return context


@method_decorator(login_required, name="dispatch")
class TopicCreateView(OwnerCreateView):  # Convention: topic_form.html
    model = Topic
    fields = ["type", "text"]


@method_decorator(login_required, name="dispatch")
class TopicUpdateView(OwnerUpdateView):  # Convention: topic_form.html
    model = Topic
    fields = ["type", "text"]


@method_decorator(login_required, name="dispatch")
class TopicDeleteView(OwnerDeleteView):  # Convention: topic_confirm_delete.html
    model = Topic


class PostDetailView(OwnerDetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["references"] = context["post"].references.all()
        return context


@method_decorator(login_required, name="dispatch")
class PostCreateView(OwnerCreateView):  # Convention: post_form.html
    model = Post
    fields = ["title", "body", "status", "url"]

    def post(self, request, pk):
        form = PostForm(data=request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.owner = get_object_or_404(Profile, user=request.user)
            new_post.topic = get_object_or_404(Topic, id=pk)
            new_post.save()
            messages.success(request, ("Post Has Been Added"))
            return redirect(reverse("notes:topic_detail", args=[pk]))


@method_decorator(login_required, name="dispatch")
class PostUpdateView(OwnerUpdateView):  # Convention: post_form.html
    model = Post
    fields = ["title", "body", "status", "url"]

    def post(self, request, pk):
        post = Post.objects.get(id=pk)
        topic = post.topic
        form = PostForm(instance=post, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, ("Post Has Been Updated"))
            return redirect(reverse("notes:topic_detail", args=[topic.id]))


@method_decorator(login_required, name="dispatch")
# Convention: post_confirm_delete.html
class PostDeleteView(SuccessMessageMixin, OwnerDeleteView):
    model = Post
    # But returnes to topic list. How can we add the topic id to this.
    success_url = reverse_lazy("notes:topic_detail")
    success_message = "Post Has Been Deleted"

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(PostDeleteView, self).delete(request, *args, **kwargs)


@login_required
def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status="published")
    sent = False

    if request.method == "POST":
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = (
                f"Read {post.title} at {post_url}\n\n"
                f"{cd['name']}'s comments: {cd['comments']}"
            )
            cwd = os.getcwd()
            if cwd == "/app" or cwd.startswith("/tmp"):
                app_id = os.environ["EMAIL_ADDRESS"]
            else:
                config = configparser.ConfigParser()
                config.read(os.path.join("D:\\Data", "API_Keys", "TPAMWeb.ini"))
                address = config["Email"]["address"]
            send_mail(subject, message, address, [cd["to"]])
            sent = True

    else:
        form = EmailPostForm()
    return render(
        request, "notes/share.html", {"post": post, "form": form, "sent": sent}
    )


def references(request):
    errors = None
    page = None

    if request.method == "POST":
        selection_criteria = ReferenceSelectionForm(request.POST)

        if selection_criteria.is_valid() and selection_criteria.cleaned_data != None:
            conditions = Q()
            cleandata = selection_criteria.cleaned_data

            if "title" in cleandata and cleandata["title"]:
                conditions &= Q(title__icontains=cleandata["title"])

            if "year" in cleandata and cleandata["year"]:
                conditions &= Q(year__icontains=str(cleandata["year"]))

            if "month" in cleandata and cleandata["month"]:
                conditions &= Q(month__icontains=str(cleandata["month"]))

            if "authors" in cleandata and cleandata["authors"]:
                conditions &= Q(authors__icontains=cleandata["authors"])

            if "editors" in cleandata and cleandata["editors"]:
                conditions &= Q(editors__icontains=cleandata["editors"])

            if "journal" in cleandata and cleandata["journal"]:
                conditions &= Q(journal__icontains=cleandata["journal"])

            if "volume" in cleandata and cleandata["volume"]:
                conditions &= Q(volume__icontains=cleandata["volume"])

            if "issue" in cleandata and cleandata["issue"]:
                conditions &= Q(issue__icontains=cleandata["issue"])

            conditions &= ~Q(type=6)

            queryset = Reference.objects.filter(conditions)

            # Convert the QuerySet to a list before storing in session
            queryset_data = serializers.serialize("json", queryset)
            request.session["ref_criteria"] = queryset_data
        else:
            errors = selection_criteria.errors or None
            queryset = (
                Reference.objects.exclude(type=6)
                .prefetch_related("person_set")
                .order_by("name")
            )

    else:
        previous_criteria_data = request.session.pop("ref_criteria", None)
        if previous_criteria_data:
            # Load the previous criteria from session and convert back to a QuerySet
            previous_criteria = list(
                serializers.deserialize("json", previous_criteria_data)
            )
        else:
            previous_criteria = None

        selection_criteria = ReferenceSelectionForm(
            initial=previous_criteria, clear_previous_criteria=True
        )
        errors = selection_criteria.errors
        queryset = Reference.objects.exclude(type=6).order_by("title")

    queryset = pagination(request, queryset)

    context = {
        "selection_criteria": selection_criteria,
        "errors": errors,
        "references": queryset,
    }

    return render(request, "notes/references.html", context)


def references(request):
    errors = None

    # Default queryset excluding type 6 and ordering by full_reference
    queryset = (
        Reference.objects.exclude(type=6)
        .prefetch_related("person_set")
        .order_by("full_reference")
    )

    # Load selection criteria from session if available
    if request.method == "POST":
        selection_criteria = ReferenceSelectionForm(request.POST)
        if selection_criteria.is_valid():
            # Save criteria to session
            request.session["reference_selection_criteria"] = request.POST.dict()
            return redirect(request.path_info)
    else:
        # Initialize form with session-stored data or empty if none available
        form_data = request.session.get("reference_selection_criteria", None)
        selection_criteria = ReferenceSelectionForm(form_data)

    # Filter queryset based on selection criteria
    if selection_criteria.is_valid():
        queryset = references_query_build(selection_criteria.cleaned_data)

    queryset = pagination(request, queryset)

    context = {
        "selection_criteria": selection_criteria,
        "errors": errors,
        "queryset": queryset,
    }
    return render(request, "notes/references.html", context)


def references_query_build(selection_criteria):

    conditions = Q()
    cleandata = selection_criteria

    if "title" in cleandata and cleandata["title"]:
        conditions &= Q(title__icontains=cleandata["title"])

    if "year" in cleandata and cleandata["year"]:
        conditions &= Q(year__icontains=str(cleandata["year"]))

    if "month" in cleandata and cleandata["month"]:
        conditions &= Q(month__icontains=str(cleandata["month"]))

    if "authors" in cleandata and cleandata["authors"]:
        conditions &= Q(authors__icontains=cleandata["authors"])

    if "editors" in cleandata and cleandata["editors"]:
        conditions &= Q(editors__icontains=cleandata["editors"])

    if "journal" in cleandata and cleandata["journal"]:
        conditions &= Q(journal__icontains=cleandata["journal"])

    if "volume" in cleandata and cleandata["volume"]:
        conditions &= Q(volume__icontains=cleandata["volume"])

    if "issue" in cleandata and cleandata["issue"]:
        conditions &= Q(issue__icontains=cleandata["issue"])

    conditions &= ~Q(type=6)

    queryset = (
        Reference.objects.filter(conditions)
        .prefetch_related("person_set")
        .order_by("full_reference")
    )

    return queryset


def reference(request, reference_id):
    reference = Reference.objects.get(id=reference_id)

    context = {
        "reference": reference,
        "references": references,
    }
    return render(request, "notes/reference.html", context)


def timeline(request):
    from locations.models import LocationEvent
    import json

    location_events = LocationEvent.objects.order_by("description")
    events = []
    groups = []
    group_set = set()
    count = 0

    for location_event in location_events:
        if location_event.route_fk:
            group = str(location_event.route_fk)
        else:
            group = "Other"

        # Collect the group information
        group_set.add(group)

        # if location_event.date:
        if location_event.datefield:
            count += 1
            # For format see https://visjs.github.io/vis-timeline/docs/timeline/#Data_Format
            event = {
                "id": count,
                "group": group,
                "content": location_event.description,
                "start": location_event.datefield.strftime("%Y/%m/%d"),
                "event.type": "point",
            }
            events.append(event)

    # Convert group_set to a sorted list
    sorted_groups = sorted(list(group_set))

    # Create group_id_mapping from the sorted list
    group_id_mapping = {group: index + 1 for index, group in enumerate(sorted_groups)}
    groups = [
        {"id": group_id_mapping[group], "content": group} for group in sorted_groups
    ]

    # Update the items to use group IDs
    for event in events:
        event["group"] = group_id_mapping[event["group"]]

    return render(
        request,
        "notes/timeline.html",
        {"timeline_json": json.dumps(events), "groups": json.dumps(groups)},
    )


def brmplans(request):

    errors = None
    queryset = BRMPlans.objects.all()

    # Load selection criteria from session if available
    if request.method == "POST":
        selection_criteria = BRMPlansImageForm(request.POST)
        if selection_criteria.is_valid():
            # Save criteria to session
            request.session["brmplans_selection_criteria"] = request.POST.dict()
            return redirect(request.path_info)
    else:
        # Initialize form with session-stored data or empty if none available
        form_data = request.session.get("brmplans_selection_criteria", None)
        selection_criteria = BRMPlansImageForm(form_data)

    # Filter queryset based on selection criteria
    if selection_criteria.is_valid():
        # queryset = Image.objects.all()
        queryset = brmplans_query_build(selection_criteria.cleaned_data)

    queryset = pagination(request, queryset, 27)

    context = {
        "selection_criteria": selection_criteria,
        "errors": errors,
        "queryset": queryset,
    }

    return render(request, "notes/brmplans.html", context)


def brmplans_query_build(selection_criteria):

    conditions = Q()
    cleandata = selection_criteria

    if "archivenumber" in cleandata and cleandata["archivenumber"]:
        conditions &= Q(archivenumber__icontains=cleandata["archivenumber"])

    if "location" in cleandata and cleandata["location"]:
        conditions &= Q(location__icontains=cleandata["location"])

    if "description" in cleandata and cleandata["description"]:
        conditions &= Q(description__icontains=cleandata["description"])

    if "tube" in cleandata and cleandata["tube"]:
        conditions &= Q(tube__icontains=cleandata["tube"])

    queryset = BRMPlans.objects.filter(conditions).order_by("archivenumber")
    return queryset


def brmplan(request, plan_id):
    plan = BRMPlans.objects.get(id=plan_id)
    context = {"plan": plan}
    return render(request, "notes/brmplan.html", context)


def brmphotos(request):

    errors = None
    queryset = BRMPhotos.objects.all()

    # Load selection criteria from session if available
    if request.method == "POST":
        selection_criteria = BRMPhotosImageForm(request.POST)
        if selection_criteria.is_valid():
            # Save criteria to session
            request.session["brmphotos_selection_criteria"] = request.POST.dict()
            return redirect(request.path_info)
    else:
        # Initialize form with session-stored data or empty if none available
        form_data = request.session.get("brmphotos_selection_criteria", None)
        selection_criteria = BRMPhotosImageForm(form_data)

    # Filter queryset based on selection criteria
    if selection_criteria.is_valid():
        # queryset = Image.objects.all()
        queryset = brmphotos_query_build(selection_criteria.cleaned_data)

    queryset = pagination(request, queryset, 27)

    context = {
        "selection_criteria": selection_criteria,
        "errors": errors,
        "queryset": queryset,
    }

    return render(request, "notes/brmphotos.html", context)


def brmphotos_query_build(selection_criteria):

    conditions = Q()
    cleandata = selection_criteria

    if "reference_number" in cleandata and cleandata["reference_number"]:
        conditions &= Q(archivenumber__icontains=cleandata["reference_number"])

    if "location" in cleandata and cleandata["location"]:
        conditions &= Q(location__icontains=cleandata["location"])

    if "lococlass" in cleandata and cleandata["lococlass"]:
        conditions &= Q(lococlass__icontains=cleandata["lococlass"])

    queryset = (
        BRMPhotos.objects.filter(conditions)
        .annotate(
            # Convert reference_number to a string and then apply LPAD
            padded_ref=Func(
                Cast(
                    F("reference_number"), output_field=CharField()
                ),  # Convert to text
                Value(6),
                Value("0"),
                function="LPAD",
                output_field=CharField(),
            ),
            image_src=Concat(
                Value("https://www.bluebell-railway-museum.co.uk/archive/photos2/"),
                Substr(
                    "padded_ref", 1, 3, output_field=CharField()
                ),  # First 3 characters
                Value("/"),
                Substr(
                    "padded_ref", 4, 3, output_field=CharField()
                ),  # Last 3 characters
                Value(".jpg"),
            ),
        )
        .order_by("reference_number")
    )

    return queryset


# def brmphoto(request, photo_id):
#     photo = BRMPhotos.objects.get(id=photo_id)
#     context = {"photo": photo}
#     return render(request, "notes/brmphoto.html", context)

# class BRMPhotoDetailView(DetailView):
#     model = BRMPhotos
#     template_name = 'notes/brmphoto_detail.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         reference_number = self.request.GET.get('ref')
#         context['reference_number'] = reference_number
#         return context

# from django.views.generic import DetailView
# from .models import BRMPhotos


class BRMPhotoDetailView(DetailView):
    model = BRMPhotos
    template_name = "notes/brmphoto.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["image_src"] = self.request.GET.get("src")

        cart_product_form = CartAddProductForm()
        context["cart_product_form"] = cart_product_form
        print(context)
        return context
