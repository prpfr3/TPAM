from django import forms
from tinymce.widgets import TinyMCE
from .models import *


class SlideAdminForm(forms.ModelForm):

    class Meta:
        model = Slide
        fields = "__all__"

        widgets = {
            "notes": TinyMCE(
                attrs={"class": "form-control tinymce-editor", "cols": 80, "rows": 30},
                mce_attrs={
                    "content_style": """
                        body {
                            margin: 8px;
                            font-size: 13px;
                        }

                        p {
                            margin: 0 0 0.75em 0;
                        }
                    """,
                    "content_css": [
                        "/static/css/bootstrap.min.css",
                        "/static/css/custom-styles.css",
                    ],
                },
            ),
        }
