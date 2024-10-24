from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField()


class QueryForm(forms.Form):
    name = forms.CharField(required=False, max_length=255, label='Company Name')
    industry = forms.CharField(required=False, max_length=255, label='Industry')
    size_range = forms.CharField(required=False, max_length=255, label='Size Range')
    locality = forms.CharField(required=False, max_length=255, label='Locality')
    country = forms.CharField(required=False, max_length=255, label='Country')
    linkedin_url = forms.URLField(required=False, label='LinkedIn URL')
    current_employee_estimate = forms.IntegerField(required=False, min_value=0, label='Current Employee Estimate')
    total_employee_estimate = forms.IntegerField(required=False, min_value=0, label='Total Employee Estimate')

