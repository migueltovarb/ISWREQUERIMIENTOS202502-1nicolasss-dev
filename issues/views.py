from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import Issue


def text_sample(request):
    context = {
        "titulo": "Descripción",
        "contenido": "Está verificación incluye tildes: á, é, í, ó, ú; eñes: ñ; signos: ¡Hola! ¿Qué tal?",
    }
    return render(request, "issues/sample.html", context)


def json_sample(request):
    data = {
        "titulo": "Descripción",
        "detalle": "Pago número único con tokenización y confirmación inmediata",
        "caracteres": ["á", "é", "í", "ó", "ú", "ñ", "¡", "¿"],
    }
    return JsonResponse(data, json_dumps_params={"ensure_ascii": False}, content_type="application/json; charset=utf-8")


def db_json(request, pk: int):
    issue = get_object_or_404(Issue, pk=pk)
    data = {
        "id": issue.pk,
        "titulo": issue.titulo,
        "descripcion": issue.descripcion,
    }
    return JsonResponse(data, json_dumps_params={"ensure_ascii": False}, content_type="application/json; charset=utf-8")
