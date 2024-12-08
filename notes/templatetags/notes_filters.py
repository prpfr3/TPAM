# notes/templatetags/notes_filters.py
from django import template

register = template.Library()


# @register.filter
# def get_field_value(obj, field_name):
#     """Returns the value of a model's field"""
#     print(f"Loading custom filter for field: {field_name}")
#     return getattr(obj, field_name)
