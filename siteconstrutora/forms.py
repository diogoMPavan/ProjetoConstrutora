from django import forms
from django.contrib.auth.forms import AuthenticationForm

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