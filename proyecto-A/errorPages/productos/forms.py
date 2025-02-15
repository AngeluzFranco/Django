# vamos a crear formularios para cada modulo de la app/modulo
from .models import Producto
from django import forms

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'precio', 'imagen']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Nombre del producto',
                'required': True,
            }),
            'precio': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Precio del producto',
                'required': True,
                'min': 1,
            }),
            'imagen': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'URL de la imagen',
                'required': True,
            }),
        }

        labes = {
            'nombre': 'Nombre del producto',
            'precio': 'Precio (MXN)',
            'imagen': 'URL de la imagen',
        }

        error_messages = {
            'nombre': {
                'required': 'Este campo es obligatorio',
            },
            'precio': {
                'required': 'Este campo es obligatorio',
                'min_value': 'El precio debe ser mayor a 0',
            },
            'imagen': {
                'required': 'Este campo es obligatorio',
            },
        }
