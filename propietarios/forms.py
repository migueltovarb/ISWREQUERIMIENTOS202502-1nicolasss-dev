from django import forms
from .models import Propietario

class PropietarioForm(forms.ModelForm):
    """Formulario para registro y edición de propietarios."""
    class Meta:
        model = Propietario
        fields = ['nombre', 'documento', 'telefono', 'correo', 'direccion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre completo'}),
            'documento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de documento'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono de contacto'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Dirección de residencia'}),
        }
    
    def clean_documento(self):
        documento = self.cleaned_data.get('documento')
        # Aquí se podrían agregar validaciones extra si fuera necesario
        return documento
