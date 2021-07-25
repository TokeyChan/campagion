from django.forms import ModelForm, Form
import django.forms as forms
from tracker.models import Template, Task, Milestone

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

class MilestoneForm(ModelForm):
    class Meta:
        model = Milestone
        fields = ['name', 'duration', 'is_external', 'department', 'completer', 'upload_name']
        labels = {
            'duration': 'Dauer (d HH:MM:SS)',
            'is_external': 'Extern',
            'completer': 'Abschlussart',
            'upload_name': 'Dateibezeichnung'
        }
        