from django import forms
from django.contrib.auth import authenticate as dj_authenticate

class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)

    def authenticate(self, request):
        return dj_authenticate(request, username=self.cleaned_data['username'], password=self.cleaned_data['password'])