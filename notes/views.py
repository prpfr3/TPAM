import configparser
import os

from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView
from mainmenu.views import pagination

from .forms import *
from .models import *


def index(request):
    return render(request, "notes/index.html")


def post_list(request):
    # Start with all posts (update to Post.published)
    posts = Post.published.all()

    # Bind GET parameters to the form
    form = PostFilterForm(request.GET or None)

    if form.is_valid():
        if topic := form.cleaned_data.get("topic"):
            posts = posts.filter(topic=topic)

    context = {
        "form": form,
        "posts": posts,
    }
    return render(request, "notes/post_list.html", context)


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["references"] = context["post"].references.all()
        return context


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

    return (
        Reference.objects.filter(conditions)
        .prefetch_related("person_set")
        .order_by("full_reference")
    )


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
        group = str(location_event.route_fk) if location_event.route_fk else "Other"
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



