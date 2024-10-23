from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField()

class QueryForm(forms.Form):
    company_name = forms.CharField(required=False, max_length=255)
    industry = forms.CharField(required=False, max_length=255)
    revenue_min = forms.DecimalField(required=False, min_value=0)
    revenue_max = forms.DecimalField(required=False, min_value=0)
