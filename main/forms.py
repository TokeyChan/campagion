from django import forms
from django.contrib.auth import authenticate as dj_authenticate
from .models import Client, Campaign

class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ['desc', 'contract', 'start_date', 'end_date', 'daily_budget']
        labels = {
            'desc': 'Beschreibung',
            'contract': 'Vertrag',
            'start_date': 'Beginndatum',
            'end_date': 'Enddatum',
            'daily_budget': 'Tagesbudget'
        }

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name']
        labels = {
            'name': 'Name'
        }

class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)

    def authenticate(self, request):
        return dj_authenticate(request, username=self.cleaned_data['username'], password=self.cleaned_data['password'])