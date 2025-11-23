from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from .forms import ReporteForm
from citas.models import Cita
from pagos.models import Pago
from mascotas.models import Mascota
from django.db.models import Count, Sum
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io
import openpyxl

def es_admin(user):
    return user.es_admin()

@login_required
@user_passes_test(es_admin)
def generar_reporte(request):
    """Vista principal para generar reportes."""
    if request.method == 'POST':
        form = ReporteForm(request.POST)
        if form.is_valid():
            tipo = form.cleaned_data['tipo_reporte']
            inicio = form.cleaned_data['fecha_inicio']
            fin = form.cleaned_data['fecha_fin']
            formato = form.cleaned_data['formato']
            
            if formato == 'PDF':
                return generar_pdf(tipo, inicio, fin)
            else:
                return generar_excel(tipo, inicio, fin)
    else:
        form = ReporteForm()
    
    return render(request, 'reportes/generar.html', {'form': form})

def generar_pdf(tipo, inicio, fin):
    """Generar reporte en PDF."""
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    
    # Encabezado
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, 750, f"Reporte: {tipo.replace('_', ' ').title()}")
    p.setFont("Helvetica", 12)
    p.drawString(50, 730, f"Periodo: {inicio} - {fin}")
    
    y = 700
    p.setFont("Helvetica", 10)
    
    if tipo == 'citas_mes':
        data = Cita.objects.filter(fecha__range=[inicio, fin]).values('fecha').annotate(total=Count('id')).order_by('fecha')
        for item in data:
            p.drawString(50, y, f"Fecha: {item['fecha']} - Total Citas: {item['total']}")
            y -= 20
            
    elif tipo == 'ingresos_mes':
        data = Pago.objects.filter(fecha_pago__date__range=[inicio, fin]).aggregate(total=Sum('monto'))
        p.drawString(50, y, f"Total Ingresos: ${data['total'] or 0}")
        
    elif tipo == 'mascotas_especie':
        data = Mascota.objects.filter(fecha_registro__date__range=[inicio, fin]).values('especie').annotate(total=Count('id'))
        for item in data:
            p.drawString(50, y, f"Especie: {item['especie']} - Total: {item['total']}")
            y -= 20
            
    p.showPage()
    p.save()
    
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="reporte_{tipo}.pdf"'
    return response

def generar_excel(tipo, inicio, fin):
    """Generar reporte en Excel."""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Reporte"
    
    ws.append(['Reporte', tipo])
    ws.append(['Periodo', f"{inicio} - {fin}"])
    ws.append([]) # Espacio
    
    if tipo == 'citas_mes':
        ws.append(['Fecha', 'Total Citas'])
        data = Cita.objects.filter(fecha__range=[inicio, fin]).values('fecha').annotate(total=Count('id')).order_by('fecha')
        for item in data:
            ws.append([item['fecha'], item['total']])
            
    elif tipo == 'ingresos_mes':
        ws.append(['Concepto', 'Monto'])
        data = Pago.objects.filter(fecha_pago__date__range=[inicio, fin]).aggregate(total=Sum('monto'))
        ws.append(['Total Ingresos', data['total'] or 0])
        
    elif tipo == 'mascotas_especie':
        ws.append(['Especie', 'Total'])
        data = Mascota.objects.filter(fecha_registro__date__range=[inicio, fin]).values('especie').annotate(total=Count('id'))
        for item in data:
            ws.append([item['especie'], item['total']])
            
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="reporte_{tipo}.xlsx"'
    wb.save(response)
    return response
