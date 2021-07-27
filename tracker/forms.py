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
    def __init__(self, global_=False, *args, **kwargs):
        super(MilestoneForm, self).__init__(*args, **kwargs)
        if not global_:
            self.fields['for_campaign'] = forms.BooleanField(label="Nur für diese Kampagne", initial=True, required=False)
    
    class Meta:
        model = Milestone
        fields = ['name', 'duration', 'is_external', 'department', 'completer', 'upload_name']
        labels = {
            'duration': 'Dauer (d HH:MM:SS)',
            'is_external': 'Extern',
            'completer': 'Abschlussart',
            'upload_name': 'Dateibezeichnung (nur bei Upload)'
        }

    def save(self, campaign_id):
        try:
            if self.cleaned_data['for_campaign']:
                self.instance.campaign_id = campaign_id
        except:
            pass
        self.instance.upload_dir = self.cleaned_data['upload_name'].lower() + "s"

        super().save()
        