from django import forms
from .models import Mascota, TransferenciaMascota
from propietarios.models import Propietario

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


class TransferenciaMascotaForm(forms.Form):
    """Formulario para transferir una mascota de un propietario a otro (HU-010)."""
    
    mascota = forms.ModelChoiceField(
        queryset=Mascota.objects.filter(activo=True),
        label='Mascota',
        widget=forms.Select(attrs={'class': 'form-select'}),
        help_text='Seleccione la mascota a transferir',
        empty_label='Seleccione una mascota...'
    )
    
    nuevo_propietario = forms.ModelChoiceField(
        queryset=Propietario.objects.all(),
        label='Nuevo Propietario',
        widget=forms.Select(attrs={'class': 'form-select'}),
        help_text='Seleccione el nuevo propietario',
        empty_label='Seleccione un propietario...'
    )
    
    motivo = forms.CharField(
        required=False,
        label='Motivo de la transferencia',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Motivo de la transferencia (opcional)'
        }),
        max_length=500
    )
    
    def clean(self):
        """Validar que no se transfiera a sí mismo."""
        cleaned_data = super().clean()
        mascota = cleaned_data.get('mascota')
        nuevo_propietario = cleaned_data.get('nuevo_propietario')
        
        if mascota and nuevo_propietario:
            if mascota.propietario == nuevo_propietario:
                raise forms.ValidationError(
                    'No se puede transferir la mascota al mismo propietario actual.'
                )
        
        return cleaned_data
