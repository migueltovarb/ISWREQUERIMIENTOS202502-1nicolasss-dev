from django import forms
from .models import Pago
from citas.models import Cita

class PagoForm(forms.ModelForm):
    """Formulario para registrar un pago."""
    
    class Meta:
        model = Pago
        fields = ['propietario', 'cita', 'monto', 'tipo_pago', 'referencia', 'ultimos_4_digitos']
        widgets = {
            'propietario': forms.Select(attrs={'class': 'form-select'}),
            'cita': forms.Select(attrs={'class': 'form-select'}),
            'monto': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Monto a pagar'}),
            'tipo_pago': forms.Select(attrs={'class': 'form-select', 'id': 'id_tipo_pago'}),
            'referencia': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'N° de referencia (opcional)'}),
            'ultimos_4_digitos': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Últimos 4 dígitos', 'maxlength': '4'}),
        }

    def __init__(self, *args, **kwargs):
        cita_id = kwargs.pop('cita_id', None)
        super().__init__(*args, **kwargs)
        
        if cita_id:
            cita = Cita.objects.get(pk=cita_id)
            self.fields['cita'].initial = cita
            self.fields['propietario'].initial = cita.propietario
            self.fields['monto'].initial = cita.servicio.precio
            # Hacer campos de solo lectura si vienen de una cita
            self.fields['cita'].disabled = True
            self.fields['propietario'].disabled = True
            self.fields['monto'].widget.attrs['readonly'] = True
