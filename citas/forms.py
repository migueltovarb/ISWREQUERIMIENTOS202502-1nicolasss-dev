from django import forms
from .models import Cita
from mascotas.models import Mascota
from propietarios.models import Propietario
from autenticacion.models import Usuario


class CitaForm(forms.ModelForm):
    """Formulario para agendar y editar citas (Staff)."""
    
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


class CitaPropietarioForm(forms.ModelForm):
    """Formulario simplificado para que propietarios agenden citas para sus mascotas."""
    
    class Meta:
        model = Cita
        fields = ['mascota', 'servicio', 'veterinario', 'fecha', 'hora', 'observaciones']
        widgets = {
            'mascota': forms.Select(attrs={'class': 'form-select'}),
            'servicio': forms.Select(attrs={'class': 'form-select'}),
            'veterinario': forms.Select(attrs={'class': 'form-select'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'hora': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3,
                'placeholder': 'Describe brevemente el motivo de la consulta o cualquier información relevante...'
            }),
        }
        labels = {
            'mascota': 'Selecciona tu mascota',
            'servicio': 'Tipo de servicio',
            'veterinario': 'Veterinario de preferencia',
            'fecha': 'Fecha deseada',
            'hora': 'Hora deseada',
            'observaciones': 'Motivo de la consulta',
        }
    
    def __init__(self, *args, propietario=None, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Importar Servicio aquí para evitar importación circular
        from servicios.models import Servicio
        
        # Filtrar servicios activos
        self.fields['servicio'].queryset = Servicio.objects.filter(activo=True)
        
        # Filtrar veterinarios activos
        self.fields['veterinario'].queryset = Usuario.objects.filter(rol='VETERINARIO', activo=True)
        self.fields['veterinario'].empty_label = "Sin preferencia (asignar automáticamente)"
        self.fields['veterinario'].required = False
        
        # Si se proporciona propietario, filtrar solo sus mascotas
        if propietario:
            self.fields['mascota'].queryset = Mascota.objects.filter(propietario=propietario)
        else:
            self.fields['mascota'].queryset = Mascota.objects.none()
        
        # Hacer observaciones obligatorias para propietarios
        self.fields['observaciones'].required = True
        
        # Agregar help text
        self.fields['fecha'].help_text = 'Selecciona la fecha en que deseas la cita'
        self.fields['hora'].help_text = 'Horario de atención: 8:00 AM - 6:00 PM'
        self.fields['veterinario'].help_text = 'Opcional: Si no seleccionas, asignaremos un veterinario disponible'
