from django import forms
from .models import EwasteReport


class EwasteReportForm(forms.ModelForm):
    class Meta:
        model = EwasteReport
        fields = [
            "product_condition",
            "working_parts",
            "non_working_parts",
            "estimated_value",
            "remarks"
        ]

        widgets = {
            "product_condition": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "e.g. Good, Damaged, Heavily Used"
            }),
            "working_parts": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "List all working parts"
            }),
            "non_working_parts": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "List all non-working parts (if any)"
            }),
            "estimated_value": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Estimated scrap value"
            }),
            "remarks": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Any additional remarks"
            }),
        }
