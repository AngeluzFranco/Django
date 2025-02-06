from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
import re
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput(
        attrs={
                'class': 'form-control',
                'placeholder': 'Contraseña',
                'pattern': '^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',
                'autocomplete': 'new-password',
                'title': 'Debe tener al menos 8 caracteres, un número y un símbolo (!, #, $, %, & o ?)',
                'required': True,
            }
        )
    )
    password2 = forms.CharField(label="Confirmar contraseña", widget=forms.PasswordInput(
        attrs={
                'class': 'form-control',
                'placeholder': 'Confirmar contraseña',
                'pattern': '^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',
                'autocomplete': 'new-password',
                'title': 'Debe coincidir con la contraseña ingresada anteriormente.',
                'required': True,
            }
        )
    )
    class Meta:
        model = CustomUser
        fields = ['email', 'name', 'surname', 'control_number', 'age', 'tel', 'password1', 'password2']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Correo institucional',
                'pattern': '^[a-zA-Z0-9]+@utez.edu.mx$',
                'title': 'Debe ser un correo institucional (@utez.edu.mx)',
                'required': True,
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre',
                'required': True,
            }),
            'surname': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Apellido',
                'required': True,
            }),
            'control_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingresa tu matrícula',
                'pattern': '^\d{5}[A-Za-z]{2}\d{3}$',
                'title': 'Formato válido: 5 números + 2 letras + 3 números',
                'required': True,
            }),
            'age': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Edad',
                'required': True,
                'min': 15,
                'max': 99,
            }),
            'tel': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Teléfono (10 dígitos)',
                'pattern': '^\d{10}$',
                'title': 'Debe ser un número de teléfono válido (10 dígitos)',
                'required': True,
            }),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not re.match(r'^[a-zA-Z0-9._%+-]+@utez\.edu\.mx$', email):
            raise forms.ValidationError("El correo debe ser del dominio @utez.edu.mx")
        return email

    def clean_control_number(self):
        control_number = self.cleaned_data.get('control_number')
        if not re.match(r'^\d{5}[A-Za-z]{2}\d{3}$', control_number):
            raise forms.ValidationError("La matrícula debe tener 5 números, 2 letras y 3 números (Ejemplo: 12345AB678)")
        return control_number

    def clean_tel(self):
        tel = self.cleaned_data.get('tel')
        if not re.match(r'^\d{10}$', tel):
            raise forms.ValidationError("El teléfono debe contener exactamente 10 dígitos")
        return tel

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if len(password) < 8:
            raise forms.ValidationError("La contraseña debe tener al menos 8 caracteres")
        if not re.search(r'\d', password):
            raise forms.ValidationError("La contraseña debe contener al menos un número")
        if not re.search(r'[!#$%&?]', password):
            raise forms.ValidationError("La contraseña debe contener al menos un símbolo (!, #, $, %, & o ?)")
        return password

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return cleaned_data


class CustomUserLoginForm(AuthenticationForm):
    username = forms.CharField(label="Correo electrónico", max_length=150)
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if email and password:
            user = authenticate(username=email, password=password)
            if not user:
                raise forms.ValidationError("Usuario o contraseña incorrectos.")
        return cleaned_data
