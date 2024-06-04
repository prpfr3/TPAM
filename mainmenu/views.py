from django.shortcuts import render
from .models import MyDjangoApp
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


def index(request):
    mydjangoapps = MyDjangoApp.objects.all().order_by("order")
    return render(request, "mainmenu/index.html", {"mydjangoapps": mydjangoapps})


def pagination(request, queryset, instances=40):
    paginator = Paginator(queryset, instances)
    page = request.GET.get("page")

    # Retain existing query parameters for pagination links
    query_params = request.GET.copy()
    if "page" in query_params:
        del query_params["page"]

    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver the last page of results
        paginated_queryset = paginator.page(paginator.num_pages)

    return (paginated_queryset, query_params)
