from django.shortcuts import render

# Create your views here.
import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_POST

from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, HttpResponseRedirect, render
from django.urls import reverse_lazy

from inspeccion.models import *
from inspeccion.forms import *

# * UNIDAD


@login_required
def unidad_lista(request):
    return render(
        request,
        "inspeccion/unidad_lista.html",
        {
            "titulo": "Unidades",
        },
    )


@login_required
def unidad_data(request):
    unidades = list(Unidad.objects.all().values())
    return JsonResponse({"data": unidades})


@login_required
def unidad_crear(request):
    if request.method == "POST":
        form = UnidadForm(request.POST)
        if form.is_valid():
            unidad = form.save()
            return HttpResponse(
                status=204,
                headers={
                    "HX-Trigger": json.dumps(
                        {
                            "showMessage": f"{unidad.simbolo} creado.",
                        }
                    )
                },
            )
    else:
        form = UnidadForm()
    return render(
        request,
        "inspeccion/unidad_form.html",
        {
            "form": form,
        },
    )


@login_required
def unidad_editar(request, pk):
    item = get_object_or_404(Unidad, pk=pk)
    if request.method == "POST":
        form = UnidadForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return HttpResponse(
                status=204,
                headers={
                    "HX-Trigger": json.dumps(
                        {
                            "showMessage": f"{item.simbolo} editado.",
                        }
                    )
                },
            )
    else:
        form = UnidadForm(instance=item)
    return render(
        request,
        "inspeccion/unidad_form.html",
        {
            "form": form,
            "item": item,
            "titulo": f"{item.simbolo}",
        },
    )


@login_required
@require_POST
def unidad_eliminar(request, pk):
    item = get_object_or_404(Unidad, pk=pk)
    item.delete()
    return HttpResponse(
        status=204,
        headers={
            "HX-Trigger": json.dumps(
                {
                    "showMessage": f"{item.simbolo} eliminado.",
                }
            )
        },
    )


# * PROPIEDAD


@login_required
def propiedad_lista(request):
    return render(
        request,
        "inspeccion/propiedad_lista.html",
        {
            "titulo": "propiedades",
        },
    )


@login_required
def propiedad_data(request):
    propiedades = list(
        Propiedad.objects.all().values(
            "id",
            "nombre",
            "unidades__simbolo",
            "categoria",
            "estado",
        )
    )
    return JsonResponse({"data": propiedades})


@login_required
def propiedad_crear(request):
    if request.method == "POST":
        form = PropiedadForm(request.POST)
        if form.is_valid():
            propiedad = form.save()
            return HttpResponse(
                status=204,
                headers={
                    "HX-Trigger": json.dumps(
                        {
                            "showMessage": f"{propiedad.nombre} creado.",
                        }
                    )
                },
            )
    else:
        form = PropiedadForm()
    return render(
        request,
        "inspeccion/propiedad_form.html",
        {
            "form": form,
        },
    )


@login_required
def propiedad_editar(request, pk):
    item = get_object_or_404(Propiedad, pk=pk)
    if request.method == "POST":
        form = PropiedadForm(request.POST, instance=item)
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
        form = PropiedadForm(instance=item)
    return render(
        request,
        "inspeccion/propiedad_form.html",
        {
            "form": form,
            "item": item,
            "titulo": f"{item.nombre}",
        },
    )


@login_required
@require_POST
def propiedad_eliminar(request, pk):
    item = get_object_or_404(Propiedad, pk=pk)
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


# * EQUIPO


@login_required
def equipo_lista(request):
    return render(
        request,
        "inspeccion/equipo_lista.html",
        {
            "titulo": "Equipos",
        },
    )


@login_required
def equipo_data(request):
    equipos = list(Equipo.objects.all().values())
    return JsonResponse({"data": equipos})


@login_required
def equipo_crear(request):
    if request.method == "POST":
        form = EquipoForm(request.POST)
        if form.is_valid():
            equipo = form.save()
            return HttpResponse(
                status=204,
                headers={
                    "HX-Trigger": json.dumps(
                        {
                            "showMessage": f"{equipo.nombre} creado.",
                        }
                    )
                },
            )
    else:
        form = EquipoForm()
    return render(
        request,
        "inspeccion/equipo_form.html",
        {
            "form": form,
        },
    )


@login_required
def equipo_editar(request, pk):
    item = get_object_or_404(Equipo, pk=pk)
    if request.method == "POST":
        form = EquipoForm(request.POST, instance=item)
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
        form = EquipoForm(instance=item)
    return render(
        request,
        "inspeccion/equipo_form.html",
        {
            "form": form,
            "item": item,
            "titulo": f"{item.nombre}",
        },
    )


@login_required
@require_POST
def equipo_eliminar(request, pk):
    item = get_object_or_404(Equipo, pk=pk)
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


# * METODO


@login_required
def metodo_lista(request):
    return render(
        request,
        "inspeccion/metodo_lista.html",
        {
            "titulo": "métodos",
        },
    )


@login_required
def metodo_data(request):
    metodos = list(
        Metodo.objects.all().values(
            "id",
            "nombre",
            "propiedad__nombre",
            "norma",
            "muestra",
            "posicion",
            "velocidad",
            "estado",
        )
    )
    return JsonResponse({"data": metodos})


@login_required
def metodo_crear(request):
    if request.method == "POST":
        form = MetodoForm(request.POST)
        if form.is_valid():
            metodo = form.save()
            return HttpResponse(
                status=204,
                headers={
                    "HX-Trigger": json.dumps(
                        {
                            "showMessage": f"{metodo.nombre} creado.",
                        }
                    )
                },
            )
    else:
        form = MetodoForm()
    return render(
        request,
        "inspeccion/metodo_form.html",
        {
            "form": form,
        },
    )


@login_required
def metodo_editar(request, pk):
    item = get_object_or_404(Metodo, pk=pk)
    if request.method == "POST":
        form = MetodoForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return HttpResponse(
                status=204,
                headers={
                    "HX-Trigger": json.dumps(
                        {
                            "instructivoDetalleChanged": None,
                            "showMessage": f"{item.nombre} editado.",
                        }
                    )
                },
            )
    else:
        form = MetodoForm(instance=item)
    return render(
        request,
        "inspeccion/metodo_form.html",
        {
            "form": form,
            "item": item,
            "titulo": f"{item.nombre}",
        },
    )


@login_required
def metodo_editar_parcial(request, pk):
    item = get_object_or_404(Metodo, pk=pk)
    if request.method == "POST":
        form = MetodoForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return HttpResponse(
                status=204,
                headers={
                    "HX-Trigger": json.dumps(
                        {
                            "metodoDetalleChanged": None,
                            "showMessage": f"{item.nombre} editado.",
                        }
                    )
                },
            )
    else:
        form = MetodoForm(instance=item)
    return render(
        request,
        "inspeccion/metodo_form.html",
        {
            "form": form,
            "item": item,
            "titulo": f"{item.nombre}",
        },
    )


@login_required
@require_POST
def metodo_eliminar(request, pk):
    item = get_object_or_404(Metodo, pk=pk)
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


@login_required
def metodo_detalle(request, pk):
    metodo = get_object_or_404(Metodo, pk=pk)
    metodo_contenido = MetodoContenido.objects.filter(metodo=metodo)
    return render(
        request,
        "inspeccion/metodo_detalle.html",
        {
            "metodo": metodo,
            "metodo_contenido": metodo_contenido,
            "titulo": f"Detalle de {metodo.nombre}",
            "salir": reverse_lazy("inspeccion:metodo_lista"),
        },
    )


@login_required
def metodo_detalle_caracteristicas(request, pk):
    metodo = get_object_or_404(Metodo, pk=pk)
    context = {"metodo": metodo}

    return render(request, "inspeccion/metodo_detalle/caracteristicas.html", context)


@login_required
def metodo_detalle_contenido(request, pk):
    metodo = get_object_or_404(Metodo, pk=pk)
    metodo_contenido = MetodoContenido.objects.filter(metodo=metodo)
    return render(
        request,
        "inspeccion/metodo_detalle/contenido.html",
        {
            "metodo": metodo,
            "metodo_contenido": metodo_contenido,
            "titulo": f"Detalle de {metodo.nombre}",
            "salir": reverse_lazy("inspeccion:metodo_lista"),
        },
    )


# * INSTRUCTIVO


@login_required
def instructivo_lista(request):
    return render(
        request,
        "inspeccion/instructivo_lista.html",
        {
            "titulo": "instructivos",
        },
    )


@login_required
def instructivo_data(request):
    instructivos = list(
        Instructivo.objects.all().values(
        )
    )
    return JsonResponse({"data": instructivos})


@login_required
def instructivo_crear(request):
    if request.method == "POST":
        form = InstructivoForm(request.POST)
        if form.is_valid():
            instructivo = form.save()
            return HttpResponse(
                status=204,
                headers={
                    "HX-Trigger": json.dumps(
                        {
                            "showMessage": f"{instructivo.nombre} creado.",
                        }
                    )
                },
            )
    else:
        form = InstructivoForm()
    return render(
        request,
        "inspeccion/instructivo_form.html",
        {
            "form": form,
        },
    )


@login_required
def instructivo_editar_parcial(request, pk):
    item = get_object_or_404(Instructivo, pk=pk)
    if request.method == "POST":
        form = InstructivoForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return HttpResponse(
                status=204,
                headers={
                    "HX-Trigger": json.dumps(
                        {
                            "instructivoDetalleChanged": None,
                            "showMessage": f"{item.nombre} editado.",
                        }
                    )
                },
            )
    else:
        form = InstructivoForm(instance=item)
    return render(
        request,
        "inspeccion/instructivo_form.html",
        {
            "form": form,
            "item": item,
            "titulo": f"{item.nombre}",
        },
    )


@login_required
def instructivo_editar(request, pk):
    item = get_object_or_404(Instructivo, pk=pk)
    if request.method == "POST":
        form = InstructivoForm(request.POST, instance=item)
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
        form = InstructivoForm(instance=item)
    return render(
        request,
        "inspeccion/instructivo_form.html",
        {
            "form": form,
            "item": item,
            "titulo": f"{item.nombre}",
        },
    )


@login_required
@require_POST
def instructivo_eliminar(request, pk):
    item = get_object_or_404(Instructivo, pk=pk)
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


@login_required
def instructivo_detalle(request, pk):
    instructivo = get_object_or_404(Instructivo, pk=pk)
    instructivo_metodos = InstructivoMetodo.objects.filter(instructivo=instructivo)
    return render(
        request,
        "inspeccion/instructivo_detalle.html",
        {
            "instructivo": instructivo,
            "instructivo_metodos": instructivo_metodos,
            "titulo": f"Detalle de {instructivo.nombre}",
            "salir": reverse_lazy("inspeccion:instructivo_lista"),
        },
    )


@login_required
def instructivo_detalle_caracteristicas(request, pk):
    instructivo = get_object_or_404(Instructivo, pk=pk)
    context = {"instructivo": instructivo}

    return render(request, "inspeccion/instructivo_detalle/caracteristicas.html", context)


@login_required
def instructivo_detalle_contenido(request, pk):
    instructivo = get_object_or_404(Instructivo, pk=pk)
    instructivo_metodos = InstructivoMetodo.objects.filter(instructivo=instructivo)
    return render(
        request,
        "inspeccion/instructivo_detalle/contenido.html",
        {
            "instructivo": instructivo,
            "instructivo_metodos": instructivo_metodos,
            "titulo": f"Detalle de {instructivo.nombre}",
            "salir": reverse_lazy("inspeccion:instructivo_lista"),
        },
    )


# * INSTRUCTIVO-METODO


@login_required
def instructivo_metodo_lista(request):
    return render(
        request,
        "inspeccion/instructivo_metodo_lista.html",
        {
            "titulo": "instructivos_metodos",
        },
    )


@login_required
def instructivo_metodo_data(request):
    instructivos_metodos = list(
        InstructivoMetodo.objects.all().values(
            "id",
            "instructivo__id",
            "metodo__id",
            "critico",
            "requerido",
            "estado",
        )
    )
    return JsonResponse({"data": instructivos_metodos})


@login_required
def instructivo_metodo_crear(request, instructivo_id):
    if request.method == "POST":
        form = InstructivoMetodoForm(request.POST)
        if form.is_valid():
            instructivo_metodo = form.save()
            return HttpResponse(
                status=204,
                headers={
                    "HX-Trigger": json.dumps(
                        {
                            "instructivoDetalleChanged": None,
                            "showMessage": f"{instructivo_metodo.instructivo} - {instructivo_metodo.metodo} creado.",
                        }
                    )
                },
            )
    else:
        instructivo = Instructivo.objects.get(id=instructivo_id)
        initial_data = {
            "instructivo": instructivo,
        }
        form = InstructivoMetodoForm(initial=initial_data)
    return render(
        request,
        "inspeccion/instructivo_metodo_form.html",
        {
            "form": form,
        },
    )


@login_required
def instructivo_metodo_editar(request, pk):
    item = get_object_or_404(InstructivoMetodo, pk=pk)
    if request.method == "POST":
        form = InstructivoMetodoForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return HttpResponse(
                status=204,
                headers={
                    "HX-Trigger": json.dumps(
                        {
                            "instructivoDetalleChanged": None,
                            "showMessage": f"{item.instructivo} - {item.metodo} editado.",
                        }
                    )
                },
            )
    else:
        form = InstructivoMetodoForm(instance=item)
    return render(
        request,
        "inspeccion/instructivo_metodo_form.html",
        {
            "form": form,
            "item": item,
            "titulo": f"{item.instructivo.id}",
        },
    )


@login_required
@require_POST
def instructivo_metodo_eliminar(request, pk):
    item = get_object_or_404(InstructivoMetodo, pk=pk)
    item.delete()
    return HttpResponse(
        status=204,
        headers={
            "HX-Trigger": json.dumps(
                {
                    "showMessage": f"{item.instructivo} - {item.metodo} eliminado.",
                }
            )
        },
    )


# * METODO-CONTENIDO


@login_required
def metodo_contenido_lista(request):
    return render(
        request,
        "inspeccion/metodo_contenido_lista.html",
        {
            "titulo": "Contenido de Métodos",
        },
    )


@login_required
def metodo_contenido_data(request):
    metodo_contenidos = list(
        MetodoContenido.objects.all().values(
            "id",
            "metodo__id",
            "tipo",
            "orden",
            "descripcion",
        )
    )
    return JsonResponse({"data": metodo_contenidos})


@login_required
def metodo_contenido_crear(request, metodo_id):
    if request.method == "POST":
        form = MetodoContenidoForm(request.POST)
        if form.is_valid():
            metodo_contenido = form.save()
            return HttpResponse(
                status=204,
                headers={
                    "HX-Trigger": json.dumps(
                        {
                            "metodoDetalleChanged": None,
                            "showMessage": f"{metodo_contenido.metodo} - {metodo_contenido.tipo} creado.",
                        }
                    )
                },
            )
    else:
        metodo = Metodo.objects.get(id=metodo_id)
        initial_data = {
            "metodo": metodo,
        }
        form = MetodoContenidoForm(initial=initial_data)
    return render(
        request,
        "inspeccion/metodo_contenido_form.html",
        {
            "form": form,
        },
    )


@login_required
def metodo_contenido_editar(request, pk):
    item = get_object_or_404(MetodoContenido, pk=pk)
    if request.method == "POST":
        form = MetodoContenidoForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return HttpResponse(
                status=204,
                headers={
                    "HX-Trigger": json.dumps(
                        {
                            "metodoDetalleChanged": None,
                            "showMessage": f"{item.metodo} - {item.tipo} editado.",
                        }
                    )
                },
            )
    else:
        form = MetodoContenidoForm(instance=item)
    return render(
        request,
        "inspeccion/metodo_contenido_form.html",
        {
            "form": form,
            "item": item,
            "titulo": f"{item.metodo.nombre}",
        },
    )


@login_required
@require_POST
def metodo_contenido_eliminar(request, pk):
    item = get_object_or_404(MetodoContenido, pk=pk)
    item.delete()
    return HttpResponse(
        status=204,
        headers={
            "HX-Trigger": json.dumps(
                {
                    "metodoDetalleChanged": None,
                    "showMessage": f"{item.metodo} - {item.tipo} eliminado.",
                }
            )
        },
    )
