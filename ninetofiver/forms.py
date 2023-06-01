from django import forms

from .models import Contract, Performance
from dal import autocomplete
# from django_select2 import forms as s2forms


class PerformanceContractForm(forms.Form):
    contract = forms.ModelChoiceField(queryset=Contract.objects.all(), widget=autocomplete.ModelSelect2(url='contract-autocomplete'))
  
  
  
# autocomplete.ModelSelect2(url='contract-autocomplete')  
  
# from django import forms
# from django_select2 import forms as s2forms

# from .models import Contract

# class ContractWidget(s2forms.ModelSelect2Widget):
#     model = Contract
#     queryset = Contract.objects.all()
#     search_fields = [
#         "name__icontains",
#     ]

# class PerformanceContractForm(forms.ModelForm):
#     class Meta:
#         model = Performance
#         fields = ("contract",)
#         widgets = { "contract": autocomplete.ModelSelect2(url='contract-autocomplete')}    