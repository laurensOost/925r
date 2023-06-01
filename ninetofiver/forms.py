from django import forms

from .models import Contract, Performance
from dal import autocomplete


class PerformanceContractForm(forms.Form):
    contract = forms.ModelChoiceField(
        queryset=Contract.objects.all(),
        widget=autocomplete.ModelSelect2(url="contract-autocomplete"),
    )
