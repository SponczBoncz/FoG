from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate

from .models import User

class LoginForm(forms.Form):
    login = forms.CharField(widget=forms.TextInput)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('login')
        password = cleaned_data.get('password')
        self.user = authenticate(username=username, password=password)
        if self.user is None:
            raise ValidationError("Nieprawidłowe hasło lub login")


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Hasło')
    password2 = forms.CharField(widget=forms.PasswordInput, max_length=64, label='Potwierdź hasło')
    class Meta:
        model = User
        fields = [
            'login',
            'email',
            'password',
        ]

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        self.fields['login'].widget.attrs['maxlength'] = 64
        self.fields['email'].widget = forms.EmailInput()
        self.fields['password'].widget.attrs['maxlength'] = 64

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password and password2 and password != password2:
            raise ValidationError("Hasła nie są takie same!")

    def save(self, commit=True):
        user = super().save(commit=False)
        # user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

