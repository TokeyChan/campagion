from django import forms
from django.contrib.auth import authenticate as dj_authenticate
from django.contrib.auth import login
from users.models import Department, PermissionGroup, Invitation
from users.mails import send_invitation_mail
from main.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, label="E-Mail")
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)

    def authenticate(self, request):
        return dj_authenticate(request, username=self.cleaned_data['username'], password=self.cleaned_data['password'])

class RegistrationForm(forms.Form):
    first_name = forms.CharField(label="Vorname:", max_length=70)
    last_name = forms.CharField(label="Nachname:", max_length=80)
    email = forms.EmailField(label="E-Mail:")
    password1 = forms.CharField(widget=forms.PasswordInput(), label="Passwort:")
    password2 = forms.CharField(widget=forms.PasswordInput(), label="Password wiederholen:")

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data.get('password1') != cleaned_data.get('password2'):
            raise ValidationError("Die Passwörter stimmen nicht überein!")
            
        password = cleaned_data.get('password1')
        validate_password(password) #raises a ValidationError if the password is not secure enough

        email = self.cleaned_data['email']

        if len(User.objects.filter(email=email)) != 0:
            self.add_error("email", "Es existiert bereits ein User mit dieser E-Mail Adresse")

    def create_user(self, request, invitation):
        user = User.objects.create_user(
            username=self.cleaned_data['email'],
            password=self.cleaned_data['password1'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            group=invitation.group,
            email=self.cleaned_data['email']
        )
        login(request, user)

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name']

def group_choices():
    try:
        return [(group.id, group.name) for group in PermissionGroup.objects.all()]
    except: return []

class InvitationForm(forms.Form):
    email = forms.EmailField(label="Bitte hier die E-Mail Adresse der einzuladenden Person eingeben")
    group = forms.IntegerField(
        label="Welcher Benutzergruppe soll dieser User angehören?",
        widget=forms.Select(choices=group_choices()),
    )

    def clean(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email=email).count() != 0:
            self.add_error("email", "Es existiert bereits ein User mit dieser E-Mail Adresse!")

    def invite(self, invitor):
        invitation = Invitation(invitor=invitor, email=self.cleaned_data['email'], group=PermissionGroup.objects.get(id=self.cleaned_data['group']))
        invitation.save()
        send_invitation_mail(invitation)

class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'group', 'profile_picture']
        
    def render(self):
        html = ""
        for field in self.fields.keys():
            hidden = field == 'profile_picture' 
            html += f"""<tr {"hidden" if hidden else ""}>
                        {self[field].errors}
                        <td><label for="{self[field].id_for_label}">{self[field].label}:</label></td>
                        <td>{self[field]}</td>
                    </tr>"""
        return html