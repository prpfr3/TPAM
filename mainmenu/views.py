from django.shortcuts import render
from .models import MyDjangoApp
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


def index(request):
    mydjangoapps = MyDjangoApp.objects.all().order_by("order")
    return render(request, "mainmenu/index.html", {"mydjangoapps": mydjangoapps})


def pagination(request, queryset):
    paginator = Paginator(queryset, 40)
    page = request.GET.get("page")
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        queryset = paginator.page(paginator.num_pages)

    return (queryset, page)
