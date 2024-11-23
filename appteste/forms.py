from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError  

class CustomLoginForm(AuthenticationForm):
    Usuário = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Nome de usuário',
            'aria-label': 'Nome de usuário'
        }),
        label='Nome de usuário',
    )
    Senha = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Senha',
            'aria-label': 'Senha'
        }),
        label='Senha',
    )
    

class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UpdateUserForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email']