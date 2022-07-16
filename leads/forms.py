from django import forms

from leads.models import Lead


class LeadModelForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = '__all__'


class LeadForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    age = forms.IntegerField(min_value=0)