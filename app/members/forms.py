from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class LoginForms(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self._user = None
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    def clean(self):
        super().clean()
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError('username or password is invalid')
        self._user = user

    @property
    def user(self):
        if self.errors:
            raise ValueError('form validation failed')
        return self._user

class SignupForms(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    def clean_username(self):
        # username unique?
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('that username is taken')
        return username

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            raise forms.ValidationError('passwords do not match')
        return password2

    # def clean(self):
    #     # password1 == password2 ?
    #     super().clean()
    #     password1 = self.cleaned_data.get('password1')
    #     password2 = self.cleaned_data.get('password2')
    #     if password1 != password2:
    #         raise forms.ValidationError('password1 and password2 does not match')

    def save(self):
        if self.errors:
            raise ValueError('Form validation failed')
        user = User.objects.create_user(username=self.cleaned_data['username'], password=self.cleaned_data['password1'])
        return user