from django.forms import ModelForm
from tracker.models import Template

class TemplateForm(ModelForm):
    class Meta:
        model = Template
        fields = ['name']
        labels = {
            'name': 'Name'
        }
