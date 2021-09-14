from django import forms
from django.db.models import Sum, Avg
from django.contrib.auth import authenticate as dj_authenticate
from django.core.exceptions import ValidationError
from django.contrib.staticfiles.storage import staticfiles_storage

from .models import Client, Campaign, MiniCampaign
from .api_models import CampaignStats
from users.models import Department
from main.models import User, Assignee
from main.contrib.widgets import DatePickerWidget

class CampaignForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CampaignForm, self).__init__(*args, **kwargs)
        self.fields['client'] = forms.ModelChoiceField(Client.objects.order_by("name"), required=True, label="Kunde")
        self.fields['children_json'] = forms.JSONField(widget=forms.HiddenInput())
        self.addons = {
            'client': f"<div class='form_addon'><img src='{staticfiles_storage.url('main/images/plus.png')}' id='add_client'></img></div>",
        }

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

        ids = [c.id for c in self.instance.children_set.all()]
        for row in self.cleaned_data['children_json']['rows']:
            print(row)
            if row['id'] is not None:
                c = MiniCampaign.objects.get(id=row['id'])
                ids.remove(row['id'])
            else:
                c = MiniCampaign(campaign=self.instance)
            c.name = row['name']
            c.api_id = row['api_id']
            c.save()
        
        MiniCampaign.objects.filter(id__in=ids).delete()

    class Meta:
        model = Campaign
        fields = ['name', 'client', 'budget', 'fee_percentage', 'campagion_budget', 'planned_start_date', 'days']
        labels = {
            'name': 'Name',
            'client': 'Kunde',
            'planned_start_date': 'Geplantes Startdatum',
            'days': 'Dauer (in Tagen)',
            'budget': 'Werbebudget',
            'campagion_budget': 'Paketpreis',
            'fee_percentage': 'Abgabe in %'
        }
        widgets = {
            'planned_start_date': DatePickerWidget()
        }
    #Diese Render method wäre nice auf allen Forms zu haben :(
    def render(self):
        html = ""
        for field in self.fields.keys():
            hidden = isinstance(self.fields[field].widget, forms.HiddenInput)
            try:
                addon = self.addons[field]
            except:
                addon = ""

            if hidden:
                html += self[field].__str__()
            else:
                html += f"""<div class="field_wrapper">
                            {self[field].errors}
                            <label for="{self[field].id_for_label}">{self[field].label}:</label>
                            <div class="widget_wrapper">
                                {self[field]}
                                {addon}
                            </div>
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

class CampaignDataForm(forms.Form):
    impressions = forms.CharField(max_length=200, label="Impressions")
    revenue = forms.CharField(max_length=200, label="Ausgaben (in €)")
    clicks = forms.CharField(max_length=200, label="Clicks")
    ctr = forms.CharField(max_length=200, label="CTR")
    ecpm = forms.CharField(max_length=200, label="eCPM")
    ecpc = forms.CharField(max_length=200, label="eCPC")
    conversions = forms.CharField(max_length=200, label="Conversions")

    def __init__(self, campaign, *args, **kwargs):
        super().__init__(*args, **kwargs)

        minicampaigns = campaign.children_set.all()
        stats = {}

        for minicampaign in minicampaigns:
            result = minicampaign.stats_set.all().aggregate(
                        impressions=Sum('impressions'), 
                        revenue=Sum('revenue'), 
                        clicks=Sum('clicks'),
                        conversions=Sum('conversions')
                    )
            if len(stats.keys()) == 0:
                stats = result
            else:
                for k, v in result.items():
                    stats[k] += v
        
        for key in self.fields.keys():
            self.fields[key].widget.attrs['readonly'] = True
            self.fields[key].initial = round(stats[key], 4)