import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_POST

from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, HttpResponseRedirect, render
from django.urls import reverse_lazy

from user.models import Persona
from user.forms import *


# Create your views here.
@login_required
def persona_lista(request):
    return render(
        request,
        "user/persona_lista.html",
        {
            "titulo": "Personas",
        },
    )


@login_required
def persona_data(request):
    personas = list(Persona.objects.all().values())
    return JsonResponse({"data": personas})


@login_required
def persona_crear(request):
    if request.method == "POST":
        form = PersonaForm(request.POST)
        if form.is_valid():
            persona = form.save()
            return HttpResponse(
                status=204,
                headers={
                    "HX-Trigger": json.dumps(
                        {
                            "showMessage": f"{persona.nombre} creado.",
                        }
                    )
                },
            )
    else:
        form = PersonaForm()
    return render(
        request,
        "user/persona_form.html",
        {
            "form": form,
        },
    )


@login_required
def persona_editar(request, pk):
    item = get_object_or_404(Persona, pk=pk)
    if request.method == "POST":
        form = PersonaForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return HttpResponse(
                status=204,
                headers={
                    "HX-Trigger": json.dumps(
                        {
                            "showMessage": f"{item.nombre} editado.",
                        }
                    )
                },
            )
    else:
        form = PersonaForm(instance=item)
    return render(
        request,
        "user/persona_form.html",
        {
            "form": form,
            "item": item,
            "titulo": f"{item.nombre}",
        },
    )


@login_required
@require_POST
def persona_eliminar(request, pk):
    item = get_object_or_404(Persona, pk=pk)
    item.delete()
    return HttpResponse(
        status=204,
        headers={
            "HX-Trigger": json.dumps(
                {
                    "showMessage": f"{item.nombre} eliminado.",
                }
            )
        },
    )
