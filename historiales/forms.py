from django import forms
from .models import HistorialClinico, ArchivoHistorial

class HistorialClinicoForm(forms.ModelForm):
    """Formulario para registro de historial clínico."""
    
    class Meta:
        model = HistorialClinico
        fields = ['fecha_consulta', 'diagnostico', 'tratamiento', 'vacunas', 'procedimientos', 'evolucion', 'peso_actual']
        widgets = {
            'fecha_consulta': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'diagnostico': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Diagnóstico detallado'}),
            'tratamiento': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Tratamiento prescrito'}),
            'vacunas': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Vacunas aplicadas (opcional)'}),
            'procedimientos': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Procedimientos realizados (opcional)'}),
            'evolucion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Evolución del paciente'}),
            'peso_actual': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Peso en Kg'}),
        }

class ArchivoHistorialForm(forms.ModelForm):
    """Formulario para subir archivos al historial."""
    
    class Meta:
        model = ArchivoHistorial
        fields = ['archivo', 'tipo', 'descripcion']
        widgets = {
            'archivo': forms.FileInput(attrs={'class': 'form-control'}),
            'tipo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Radiografía, Examen de sangre'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descripción breve'}),
        }
