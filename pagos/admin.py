from django.contrib import admin
from .models import Pago, Factura

class FacturaInline(admin.StackedInline):
    model = Factura
    extra = 0

@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ('fecha_pago', 'propietario', 'monto', 'tipo_pago', 'estado')
    list_filter = ('tipo_pago', 'estado', 'fecha_pago')
    inlines = [FacturaInline]

@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ('numero_factura', 'fecha_emision', 'propietario', 'total')
