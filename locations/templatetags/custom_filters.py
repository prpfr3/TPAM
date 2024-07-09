from django import template

register = template.Library()


@register.filter
def startswith(value, arg):
    return str(value).startswith(arg)


@register.inclusion_tag("locations/slice_column.html")
def render_slice(queryset, start, end):
    sliced_queryset = queryset[start:end]
    return {"sliced_queryset": sliced_queryset}
