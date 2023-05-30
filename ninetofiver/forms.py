from django import forms

from .models import Contract


class PerformanceContractForm(forms.Form):
    contract = forms.ModelChoiceField(queryset=Contract.objects.all())
