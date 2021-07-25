from django import forms
from django.contrib.auth import authenticate as dj_authenticate
from .models import Client, Campaign
from users.models import Department

class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ['desc', 'start_date', 'end_date', 'daily_budget']
        labels = {
            'desc': 'Beschreibung',
            'start_date': 'Beginndatum',
            'end_date': 'Enddatum',
            'daily_budget': 'Tagesbudget'
        }
    #Diese Render method wäre nice auf allen Forms zu haben :(
    def render(self):
        html = ""
        for field in self.fields.keys():
            html += f"""<div class="field_wrapper">
                        {self[field].errors}
                        <label for="{self[field].id_for_label}">{self[field].label}:</label><br>
                        {self[field]}
                    </div>"""
        return html

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'contact_name', 'phone', 'email']
        labels = {
            'name': 'Name',
            'contact_name': 'Name der Kontaktperson',
            'phone': 'Telefonnummer',
            'email': 'E-Mail Adresse'
        }

class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)

    def authenticate(self, request):
        return dj_authenticate(request, username=self.cleaned_data['username'], password=self.cleaned_data['password'])