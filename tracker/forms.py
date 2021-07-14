from django.forms import ModelForm, Form
import django.forms as forms
from tracker.models import Template, Task

class TemplateForm(ModelForm):
    class Meta:
        model = Template
        fields = ['name']
        labels = {
            'name': 'Name'
        }

class UploadForm(ModelForm):
    class Meta:
        model = Task
        fields = ['uploaded_file']
        labels = {
            'uploaded_file': 'Datei'
        }