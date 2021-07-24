from django import forms
from django.contrib.auth import authenticate as dj_authenticate
from users.models import Department, PermissionGroup
from users.mails import send_invitation_mail

class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)

    def authenticate(self, request):
        return dj_authenticate(request, username=self.cleaned_data['username'], password=self.cleaned_data['password'])


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = [
            'name'
        ]
        labels = {
            'name': 'Name'
        }

class InvitationForm(forms.Form):
    email = forms.EmailField(label="Bitte hier die E-Mail Adresse der einzuladenden Person eingeben")
    group = forms.IntegerField(
        label="Welcher Benutzergruppe soll dieser User angehören?",
        widget=forms.Select(choices=[(group.id, group.name) for group in PermissionGroup.objects.all()]),
    )

    def invite(self):
        send_invitation_mail(self.cleaned_data['email'])