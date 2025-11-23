from django import forms

class ReporteForm(forms.Form):
    """Formulario para generar reportes."""
    
    TIPO_REPORTE_CHOICES = [
        ('citas_mes', 'Citas por Mes'),
        ('ingresos_mes', 'Ingresos por Mes'),
        ('mascotas_especie', 'Mascotas por Especie'),
    ]
    
    FORMATO_CHOICES = [
        ('PDF', 'PDF'),
        ('EXCEL', 'Excel'),
    ]
    
    tipo_reporte = forms.ChoiceField(choices=TIPO_REPORTE_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    fecha_inicio = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    fecha_fin = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    formato = forms.ChoiceField(choices=FORMATO_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
