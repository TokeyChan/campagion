from django import forms
from django.contrib.auth import authenticate as dj_authenticate
from django.core.exceptions import ValidationError
from .models import Client, Campaign
from .api_models import CampaignStats
from users.models import Department
from main.models import User, Assignee

class CampaignForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CampaignForm, self).__init__(*args, **kwargs)

        for department in Department.objects.all():

            try:
                assignee = Assignee.objects.get(campaign=self.instance, department=department)
            except Assignee.DoesNotExist:
                assignee = None

            self.fields[f'assignee_{department.id}'] = forms.IntegerField(
                label=f"Verantwortlich für {department.name}",
                widget=forms.Select(choices=[(-1, "----------------")] + [(user.id, user.name()) for user in User.objects.all()])
            )
            if assignee != None:
                self.fields[f'assignee_{department.id}'].initial = assignee.user.id


    def clean(self):
        self.assignee_datas = [(int(data[0].split('_')[-1]), data[1]) for data in self.cleaned_data.items() if 'assignee' in data[0]]
        
        for data in self.assignee_datas:
            if data[1] == -1:
                raise ValidationError("Zu jedem Department muss ein User ausgewählt sein!")

    def save(self):
        super(CampaignForm, self).save()

        for data in self.assignee_datas:
            department = Department.objects.get(id=data[0])
            user = User.objects.get(id=data[1])

            try:
                assignee = Assignee.objects.get(department=department, user=user, campaign=self.instance)
            except Assignee.DoesNotExist:
                previous = Assignee.objects.filter(campaign=self.instance, department=department)
                if len(previous) == 1: #Wenn es schon eine Assignte Person gibt
                    previous[0].user = user
                    previous[0].save()
                else:
                    assignee = Assignee(department=department, user=user, campaign=self.instance)
                    assignee.save()


    class Meta:
        model = Campaign
        fields = ['name', 'client', 'budget', 'campagion_budget', 'planned_start_date', 'days', 'api_id']
        labels = {
            'name': 'Name',
            'client': 'Kunde',
            'planned_start_date': 'Geplantes Startdatum',
            'days': 'Dauer (in Tagen)',
            'budget': 'Gesamtbudget',
            'campagion_budget': 'Campagion-Budget',
            'api_id': 'API-ID (optional)'
        }
    #Diese Render method wäre nice auf allen Forms zu haben :(
    def render(self):
        html = ""
        for field in self.fields.keys():
            html += f"""<div class="field_wrapper">
                        {self[field].errors}
                        <label for="{self[field].id_for_label}">{self[field].label}:</label>
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

class CampaignDataForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CampaignDataForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.disabled = True

    class Meta:
        model = CampaignStats
        fields = ['impressions', 'revenue', 'clicks', 'ctr', 'ecpm', 'ecpc']
        labels = {
            'revenue': 'Ausgaben (in €)',
            'ctr': 'ctr',
            'ecpm': 'ecpm',
            'ecpc': 'ecpc'
        }
        widgets = {field:forms.TextInput() for field in fields}

    def render(self):
        html = ""
        for field in self.fields.keys():
            html += f"""<div class="field_wrapper">
                        {self[field].errors}
                        <label for="{self[field].id_for_label}">{self[field].label}:</label>
                        {self[field]}
                    </div>"""
        return html