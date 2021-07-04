from django.forms import ModelForm
from .models import Client, Campaign

class CampaignForm(ModelForm):
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
