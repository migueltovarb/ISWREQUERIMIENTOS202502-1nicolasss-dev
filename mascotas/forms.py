from django import forms
from .models import Mascota

class MascotaForm(forms.ModelForm):
    """Formulario para registro y edición de mascotas."""
    class Meta:
        model = Mascota
        fields = ['nombre', 'especie', 'raza', 'edad', 'peso', 'sexo', 'foto', 'observaciones']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la mascota'}),
            'especie': forms.Select(attrs={'class': 'form-select'}),
            'raza': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Raza'}),
            'edad': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Edad en años'}),
            'peso': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Peso en Kg', 'step': '0.1'}),
            'sexo': forms.Select(attrs={'class': 'form-select'}),
            'foto': forms.FileInput(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Observaciones adicionales'}),
        }
