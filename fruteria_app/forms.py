import re
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Empleado

class EmpleadoRegistrationForm(forms.Form):
    username = forms.CharField(
        label="Usuario",
        min_length=5,
        max_length=20,
        help_text="Entre 5 y 20 caracteres."
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput,
        min_length=8
    )
    confirm_password = forms.CharField(
        label="Confirmar Contraseña",
        widget=forms.PasswordInput
    )
    nombre = forms.CharField(
        label="Nombre Completo",
        min_length=3,
        max_length=60
    )
    turno = forms.CharField(label="Turno", required=False)
    salario = forms.DecimalField(
        label="Salario", 
        required=False,
        widget=forms.NumberInput(attrs={'step': '0.01'}) 
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += ' form-control'
            else:
                field.widget.attrs['class'] = 'form-control'            
            field.widget.attrs['placeholder'] = field.label

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if Empleado.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nombre de usuario ya está en uso.")
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not (re.search(r'[A-Z]', password) and \
                re.search(r'[a-z]', password) and \
                re.search(r'\d', password)):
            raise forms.ValidationError("La contraseña debe tener al menos 8 caracteres, una mayúscula, una minúscula y un número.")
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        
        return cleaned_data


class LoginForm(AuthenticationForm):    
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Usuario',
        }
    ))
    
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña',
        }
    ))

    error_messages = {
        "invalid_login": "Por favor ingresa un usuario y contraseña correctos.",
        "inactive": "Esta cuenta está inactiva.",
    }