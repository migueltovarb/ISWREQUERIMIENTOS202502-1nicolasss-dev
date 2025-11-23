from django import forms
from .models import Cita
from mascotas.models import Mascota
from propietarios.models import Propietario
from autenticacion.models import Usuario

class CitaForm(forms.ModelForm):
    """Formulario para agendar y editar citas."""
    
    class Meta:
        model = Cita
        fields = ['propietario', 'mascota', 'servicio', 'veterinario', 'fecha', 'hora', 'observaciones', 'es_emergencia']
        widgets = {
            'propietario': forms.Select(attrs={'class': 'form-select', 'id': 'id_propietario'}),
            'mascota': forms.Select(attrs={'class': 'form-select', 'id': 'id_mascota'}),
            'servicio': forms.Select(attrs={'class': 'form-select'}),
            'veterinario': forms.Select(attrs={'class': 'form-select'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'hora': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'es_emergencia': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Importar Servicio aquí para evitar importación circular
        from servicios.models import Servicio
        
        # Filtrar servicios activos
        self.fields['servicio'].queryset = Servicio.objects.filter(activo=True)
        
        # Filtrar veterinarios activos
        self.fields['veterinario'].queryset = Usuario.objects.filter(rol='VETERINARIO', activo=True)
        
        # Lógica para filtrar mascotas si se selecciona propietario (básica para carga inicial)
        if 'propietario' in self.data:
            try:
                propietario_id = int(self.data.get('propietario'))
                self.fields['mascota'].queryset = Mascota.objects.filter(propietario_id=propietario_id)
            except (ValueError, TypeError):
                pass  # Valor inválido, usar queryset por defecto
        elif self.instance.pk:
            self.fields['mascota'].queryset = self.instance.propietario.mascotas.all()
        else:
            self.fields['mascota'].queryset = Mascota.objects.none()
