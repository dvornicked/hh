from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            qs = User.objects.filter(username=username)
            if not qs.exists():
                raise forms.ValidationError("This user does not exist")
            if not check_password(password, qs.first().password):
                raise forms.ValidationError("Incorrect password")
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("This user is not active")
        return super(LoginForm, self).clean(*args, **kwargs)
