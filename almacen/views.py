import csv
import json

from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, HttpResponseRedirect, render

from almacen.forms import *
from almacen.models import *
from core.forms import *


# * CARACTERÍSTICA


@login_required
def caracteristica_lista(request):
    return render(
        request,
        "almacen/caracteristica_lista.html",
        {
            "titulo": "caracteristicas",
        },
    )


@login_required
def caracteristica_data(request):
    caracteristicas = list(Caracteristica.objects.all().values())
    return JsonResponse({"data": caracteristicas})


@login_required
def caracteristica_crear(request):
    if request.method == "POST":
        form = CaracteristicaForm(request.POST)
        if form.is_valid():
            caracteristica = form.save()
            return HttpResponse(
                status=204,
                headers={
                    "HX-Trigger": json.dumps(
                        {
                            "showMessage": f"{caracteristica.nombre} creado.",
                        }
                    )
                },
            )
    else:
        form = CaracteristicaForm()
    return render(
        request,
        "almacen/caracteristica_form.html",
        {
            "form": form,
        },
    )


@login_required
def caracteristica_editar(request, pk):
    item = get_object_or_404(Caracteristica, pk=pk)
    if request.method == "POST":
        form = CaracteristicaForm(request.POST, instance=item)
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
        form = CaracteristicaForm(instance=item)
    return render(
        request,
        "almacen/caracteristica_form.html",
        {
            "form": form,
            "item": item,
            "titulo": f"{item.nombre}",
        },
    )


@login_required
@require_POST
def caracteristica_eliminar(request, pk):
    item = get_object_or_404(Caracteristica, pk=pk)
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


def seleccionar_caracteristica(request):
    # Obtenemos la lista de IDs ya seleccionados que nos envía el frontend
    # request.POST.getlist('caracteristicas') obtiene todos los valores con ese nombre
    pks_seleccionados = request.POST.getlist("caracteristicas")

    # Obtenemos el ID de la nueva característica que se acaba de cliquear
    pk_nueva_caracteristica = request.POST.get("caracteristica_id")

    # Añadimos la nueva a la lista (si no estaba ya)
    if pk_nueva_caracteristica and pk_nueva_caracteristica not in pks_seleccionados:
        pks_seleccionados.append(pk_nueva_caracteristica)

    # Convertimos los IDs (que son strings) a enteros para la consulta
    pks_seleccionados_int = [int(pk) for pk in pks_seleccionados if pk]

    # Calculamos las nuevas listas
    caracteristicas_seleccionadas = Caracteristica.objects.filter(
        pk__in=pks_seleccionados_int
    )
    caracteristicas_disponibles = Caracteristica.objects.exclude(
        pk__in=pks_seleccionados_int
    )

    # Preparamos el contexto para las plantillas parciales
    context = {
        "caracteristicas_seleccionadas": caracteristicas_seleccionadas,
        "caracteristicas_disponibles": caracteristicas_disponibles,
    }

    # Renderizamos y devolvemos AMBOS partials.
    # El usuario de django-htmx haría esto más fácil, pero vamos a hacerlo manualmente
    # para que se entienda.

    # Esto requiere que tus partials estén envueltos en un contenedor
    # para que el swap 'outerHTML' funcione bien.
    return render(request, "almacen/partials/contenedor_caracteristicas.html", context)


def deseleccionar_caracteristica(request):
    pks_seleccionados = request.POST.getlist("caracteristicas")
    pk_a_quitar = request.POST.get("caracteristica_id")

    # Quitamos la característica de la lista
    if pk_a_quitar in pks_seleccionados:
        pks_seleccionados.remove(pk_a_quitar)

    pks_seleccionados_int = [int(pk) for pk in pks_seleccionados if pk]

    caracteristicas_seleccionadas = Caracteristica.objects.filter(
        pk__in=pks_seleccionados_int
    )
    caracteristicas_disponibles = Caracteristica.objects.exclude(
        pk__in=pks_seleccionados_int
    )

    context = {
        "caracteristicas_seleccionadas": caracteristicas_seleccionadas,
        "caracteristicas_disponibles": caracteristicas_disponibles,
    }

    return render(request, "almacen/partials/contenedor_caracteristicas.html", context)


# * CATEGORÍA


@login_required
def categoria_materia_lista(request):
    return render(
        request,
        "almacen/categoria_materia_lista.html",  # Tu plantilla HTML
        {
            "titulo": "Categorías de Materia Prima",
        },
    )


@login_required
def categoria_materia_data(request):
    categorias = list(
        CategoriaMateria.objects.all().values(
            "id",
            "nombre",
            "abreviatura",
            "bloque",
            "estado",
        )
    )

    return JsonResponse({"data": categorias})


@login_required
def categoria_materia_crear(request):
    if request.method == "POST":
        form = CategoriaMateriaForm(request.POST)
        if form.is_valid():
            categoria = form.save()
            return HttpResponse(
                status=204,
                headers={"HX-Trigger": json.dumps({"showMessage": f"{categoria.nombre} creado."})},
            )
    else:
        form = CategoriaMateriaForm()

    return render(request, "almacen/categoria_materia_form.html", {"form": form})


@login_required
def categoria_materia_editar(request, pk):
    item = get_object_or_404(CategoriaMateria, pk=pk)
    if request.method == "POST":
        form = CategoriaMateriaForm(request.POST, instance=item)
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
        form = CategoriaMateriaForm(instance=item)
    # La lógica de contexto es diferente aquí
    seleccionadas = item.caracteristicas.all()
    disponibles = Caracteristica.objects.exclude(pk__in=seleccionadas.values_list("pk"))
    return render(
        request,
        "almacen/categoria_materia_form.html",
        {
            "form": form,
            "item": item,
            "titulo": f"{item.nombre}",
            "caracteristicas_seleccionadas": seleccionadas,
            "caracteristicas_disponibles": disponibles,
        },
    )


@login_required
@require_POST
def categoria_materia_eliminar(request, pk):
    item = get_object_or_404(CategoriaMateria, pk=pk)
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


# * MATERIA


@login_required
def materia_lista(request):
    return render(
        request,
        "almacen/materia_lista_sp.html",  # Tu plantilla HTML
        {
            "titulo": "Materias Primas",
        },
    )


@login_required
def materia_data(request):
    materias = list(
        Materia.objects.all().values(
            "id",
            "nombre",
            "categoria__nombre",
            # "tipo",
            # "composicion",
            # "construccion",
            # "caracteristica",
            # "brillo",
            # "grabado",
            # "pasadas",
            # "factor",
            # "espesor",
            # "peso",
            # "ancho",
            "costo",
            "date_updated",
            "estado",
        )
    )
    return JsonResponse({"data": materias})


@login_required
def materia_crear(request):
    if request.method == "POST":
        form = MateriaForm(request.POST)
        if form.is_valid():
            materia = form.save()
            # Ahora, iteramos sobre los datos del POST para encontrar nuestras características
            for key, value in request.POST.items():
                if key.startswith('caracteristica_'):
                    # Si el input se llama 'caracteristica_5', el id es 5
                    caracteristica_id = int(key.split('_')[1])
                    
                    # Si el usuario ha introducido un valor
                    if value:
                        # Creamos o actualizamos el objeto ValorCaracteristicaMateria
                        CaracteristicaMateria.objects.update_or_create(
                            materia=materia,
                            caracteristica_id=caracteristica_id,
                            defaults={'valor': value}
                        )
            return HttpResponse(
                status=204,
                headers={
                    "HX-Trigger": json.dumps(
                        {
                            "showMessage": f"{materia.nombre} creado.",
                        }
                    )
                },
            )
    else:
        form = MateriaForm()
    return render(
        request,
        "almacen/materia_form.html",
        {
            "form": form,
        },
    )


@login_required
def materia_editar(request, pk):
    item = get_object_or_404(Materia, pk=pk)
    if request.method == "POST":
        form = MateriaForm(request.POST, instance=item)
        if form.is_valid():
            materia = form.save() # Guardamos los cambios en Materia (nombre, costo, etc.)
            # --- LÓGICA DE GUARDADO DE CARACTERÍSTICAS (¡Igual que en crear!) ---
            for key, value in request.POST.items():
                if key.startswith('caracteristica_'):
                    caracteristica_id = int(key.split('_')[1])
                    
                    # Si el valor no está vacío, lo guardamos/actualizamos
                    if value:
                        CaracteristicaMateria.objects.update_or_create(
                            materia=materia,
                            caracteristica_id=caracteristica_id,
                            defaults={'valor': value}
                        )
                    # Si el valor está vacío, eliminamos la entrada si existe
                    else:
                        CaracteristicaMateria.objects.filter(
                            materia=materia,
                            caracteristica_id=caracteristica_id
                        ).delete()
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
        form = MateriaForm(instance=item)

    # --- LÓGICA DE PREPARACIÓN DEL CONTEXTO (PARA GET y POST inválido) ---
    
    # 1. Obtenemos la plantilla de características desde la categoría de la materia
    caracteristicas_plantilla = item.categoria.caracteristicas.all() # o .caracteristicas_plantilla

    # 2. Obtenemos los valores que YA están guardados para esta materia en un diccionario
    #    para un acceso rápido. Ej: {5: 'Rojo', 8: '150 HB'}
    valores_guardados = {
        vc.caracteristica_id: vc.valor
        for vc in item.valores_caracteristicas.all()
    }
    
    # 3. "Hidratamos" la plantilla con los valores guardados
    #    Creamos una lista de objetos característica a la que le añadimos un atributo temporal
    caracteristicas_con_valores = []
    for c in caracteristicas_plantilla:
        c.valor_actual = valores_guardados.get(c.id, "") # Usamos .get() para evitar errores
        caracteristicas_con_valores.append(c)

    # 4. Construimos el contexto final
    context = {
        "form": form,
        "item": item,
        "object": item, # Es buena práctica incluir 'object' también
        "titulo": f"{item.nombre}",
        # ¡La variable clave que le faltaba a tu plantilla parcial!
        "caracteristicas": caracteristicas_con_valores, 
    }

    # 5. Renderizamos la plantilla con el contexto completo
    return render(request, "almacen/materia_form.html", context)


@login_required
@require_POST
def materia_eliminar(request, pk):
    item = get_object_or_404(Materia, pk=pk)
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
def materia_clonar(request, pk):
    objeto_a_clonar = get_object_or_404(Materia, pk=pk)
    if request.method == "POST":
        form = MateriaClonarForm(request.POST)
        if form.is_valid():
            objeto_nuevo_id = form.cleaned_data["nuevo_id"]
            if Materia.objects.filter(id=objeto_nuevo_id).exists():
                form.add_error("nuevo_id", "El código ya existe.")
                response = render(
                    request,
                    "almacen/materia_clonar.html",
                    {"form": form, "objeto_a_clonar": objeto_a_clonar},
                )
                return response
            else:
                objeto_nuevo = Materia(
                    id=objeto_nuevo_id,
                    nombre=f"{objeto_a_clonar.id} (Clonado)",
                    categoria=objeto_a_clonar.categoria,
                    tipo=objeto_a_clonar.tipo,
                    composicion=objeto_a_clonar.composicion,
                    construccion=objeto_a_clonar.construccion,
                    caracteristica=objeto_a_clonar.caracteristica,
                    brillo=objeto_a_clonar.brillo,
                    grabado=objeto_a_clonar.grabado,
                    pasadas=objeto_a_clonar.pasadas,
                    espesor=objeto_a_clonar.espesor,
                    peso=objeto_a_clonar.peso,
                    ancho=objeto_a_clonar.ancho,
                    costo=objeto_a_clonar.costo,
                    estado=objeto_a_clonar.estado,
                    obs=objeto_a_clonar.obs,
                )
                objeto_nuevo.save()
                return HttpResponse(
                    status=204,
                    headers={
                        "HX-Trigger": json.dumps(
                            {
                                "showMessage": f"Se ha generado el objeto: {objeto_nuevo_id}",
                            }
                        )
                    },
                )
    else:
        form = MateriaClonarForm()

    return render(
        request,
        "almacen/materia_clonar_form.html",
        {
            "form": form,
            "titulo": f"Clonar {objeto_a_clonar}",
        },
    )


@login_required
def materia_costo_bloque(request):
    if request.method == "POST":
        form = MateriaCostoBloqueForm(request.POST)
        if form.is_valid():
            categoria_objetivo = form.cleaned_data["categoria_objetivo"]
            costo_bloque = form.cleaned_data["costo_bloque"]
            items_actualizar = Materia.objects.filter(
                categoria=categoria_objetivo
            ).update(costo=costo_bloque)
            return HttpResponse(
                status=204,
                headers={
                    "HX-Trigger": json.dumps(
                        {
                            "showMessage": f"Se ha actualizado el costo de la categoría: {categoria_objetivo}, al costo {costo_bloque}, total {items_actualizar} items",
                        }
                    )
                },
            )
    else:
        form = MateriaCostoBloqueForm()
    return render(
        request,
        "almacen/materia_bloque_form.html",
        {
            "form": form,
        },
    )


@login_required
def materia_desactivar(request, pk):
    objeto_a_desactivar = get_object_or_404(Materia, pk=pk)
    objeto_a_desactivar.estado = False
    objeto_a_desactivar.save()
    return HttpResponse(
        status=204,
        headers={
            "HX-Trigger": json.dumps(
                {
                    "showMessage": f"Se ha desactivado el objeto: {objeto_a_desactivar}",
                }
            )
        },
    )


@login_required
def materia_importar(request):
    if request.method == "POST":
        form = ImportarForm(request.POST, request.FILES)
        # Agregar depuración para verificar si el archivo CSV llega al servidor
        if form.is_valid():
            csv_file = request.FILES["csv_file"]
            try:
                # Procesar el archivo CSV dentro de una transacción
                with transaction.atomic():
                    reader = csv.DictReader(
                        csv_file.read().decode("utf-8").splitlines(),
                        delimiter=";",  # Especificamos el delimitador como ";"
                    )
                    nuevas_materias = []  # Lista para bulk_create
                    materias_a_actualizar = []  # Lista para bulk_update
                    materias_existentes = (
                        {}
                    )  # Diccionario para buscar materias existentes de una vez

                    # Obtener todos los ids del CSV para buscar las materias existentes de una sola vez
                    ids_materias_csv = [row["id"] for row in reader]
                    # Reseteamos el puntero del archivo CSV para leer nuevamente
                    csv_file.seek(0)
                    reader = csv.DictReader(
                        csv_file.read().decode("utf-8").splitlines(),
                        delimiter=";",  # Especificamos el delimitador como ";"
                    )
                    # Buscar todas las materias existentes con esos ids
                    materias_en_bd = Materia.objects.filter(id__in=ids_materias_csv)
                    for materia in materias_en_bd:
                        materias_existentes[materia.id] = materia

                    for row in reader:
                        materia_id = row["id"]
                        categoria_id = row["categoria"]

                        try:
                            categoria = CategoriaMateria.objects.get(id=categoria_id)
                        except CategoriaMateria.DoesNotExist:
                            continue  # Si la categoría no existe, saltamos esta fila

                        if materia_id in materias_existentes:
                            # Actualizamos los campos para las materias que ya existen
                            materia = materias_existentes[materia_id]
                            materia.nombre = row["nombre"]
                            materia.tipo = row["tipo"]
                            materia.composicion = row["composicion"]
                            materia.construccion = row["construccion"]
                            materia.caracteristica = row["caracteristica"]
                            materia.brillo = row["brillo"]
                            materia.grabado = row["grabado"]
                            materia.pasadas = row["pasadas"]
                            materia.factor = row["factor"]
                            materia.espesor = row["espesor"]
                            materia.peso = row["peso"]
                            materia.ancho = row["ancho"]
                            materia.costo = row["costo"]

                            # Añadimos a la lista para hacer bulk_update
                            materias_a_actualizar.append(materia)
                        else:
                            # Creamos una nueva materia
                            nueva_materia = Materia(
                                id=materia_id,
                                categoria=categoria,
                                nombre=row["nombre"],
                                tipo=row["tipo"],
                                composicion=row["composicion"],
                                construccion=row["construccion"],
                                caracteristica=row["caracteristica"],
                                brillo=row["brillo"],
                                grabado=row["grabado"],
                                pasadas=row["pasadas"],
                                factor=row["factor"],
                                espesor=row["espesor"],
                                peso=row["peso"],
                                ancho=row["ancho"],
                                costo=row["costo"],
                            )

                            # Añadimos a la lista para hacer bulk_create
                            nuevas_materias.append(nueva_materia)

                    # Realizamos la creación masiva
                    if nuevas_materias:
                        Materia.objects.bulk_create(nuevas_materias)

                    # Realizamos la actualización masiva
                    if materias_a_actualizar:
                        # Solo especificamos los campos que necesitamos actualizar
                        Materia.objects.bulk_update(
                            materias_a_actualizar,
                            [
                                "nombre",
                                "tipo",
                                "composicion",
                                "construccion",
                                "caracteristica",
                                "brillo",
                                "grabado",
                                "pasadas",
                                "factor",
                                "espesor",
                                "peso",
                                "ancho",
                                "costo",
                            ],
                        )

                    return HttpResponse(
                        status=204,
                        headers={
                            "HX-Trigger": json.dumps(
                                {"showMessage": "Datos importados"}
                            )
                        },
                    )
            except Exception as e:
                return HttpResponse(
                    status=204,
                    headers={"HX-Trigger": json.dumps({"showMessage": str(e)})},
                )
    else:
        form = ImportarForm()

    return render(
        request,
        "bases/form_modal_importar.html",
        {"form": form, "titulo": "Cargar Archivo"},
    )


def htmx_materia_caracteristicas(request):
    """
    Vista llamada por HTMX cuando el usuario selecciona una categoría
    en el formulario de Materia. Devuelve los campos de input para
    las características de esa categoría.
    """
    categoria_id = request.GET.get('categoria')
    materia_id = request.GET.get('materia_id') # Para el caso de edición

    if not categoria_id:
        return HttpResponse("")

    categoria = CategoriaMateria.objects.get(pk=categoria_id)
    caracteristicas = categoria.caracteristicas.all() # O 'caracteristicas_plantilla'
    
    # Si estamos editando una materia, necesitamos obtener sus valores actuales
    if materia_id:
        materia = Materia.objects.get(pk=materia_id)
        valores_actuales = {
            vc.caracteristica_id: vc.valor 
            for vc in materia.valores_caracteristicas.all()
        }
        # Añadimos el valor actual a cada característica para pasarlo a la plantilla
        for c in caracteristicas:
            c.valor_actual = valores_actuales.get(c.id)

    context = {
        'caracteristicas': caracteristicas
    }
    return render(request, 'almacen/partials/campos_caracteristicas_valores.html', context)


# * PROVEEDOR


# @login_required
# def proveedor_lista(request):
#     return render(
#         request,
#         "almacen/proveedor_lista.html",
#         {
#             "titulo": "Proveedores",
#         },
#     )


# @login_required
# def proveedor_data(request):
#     proveedores = list(Proveedor.objects.all().values())
#     return JsonResponse({"data": proveedores})


# @login_required
# def proveedor_crear(request):
#     if request.method == "POST":
#         form = ProveedorForm(request.POST)
#         if form.is_valid():
#             proveedor = form.save()
#             return HttpResponse(
#                 status=204,
#                 headers={
#                     "HX-Trigger": json.dumps(
#                         {
#                             "showMessage": f"{proveedor.nombre} creado.",
#                         }
#                     )
#                 },
#             )
#     else:
#         form = ProveedorForm()
#     return render(
#         request,
#         "almacen/proveedor_form.html",
#         {
#             "form": form,
#         },
#     )


# @login_required
# def proveedor_editar(request, pk):
#     item = get_object_or_404(Proveedor, pk=pk)
#     if request.method == "POST":
#         form = ProveedorForm(request.POST, instance=item)
#         if form.is_valid():
#             form.save()
#             return HttpResponse(
#                 status=204,
#                 headers={
#                     "HX-Trigger": json.dumps(
#                         {
#                             "showMessage": f"{item.nombre} editado.",
#                         }
#                     )
#                 },
#             )
#     else:
#         form = ProveedorForm(instance=item)
#     return render(
#         request,
#         "almacen/proveedor_form.html",
#         {
#             "form": form,
#             "item": item,
#             "titulo": f"{item.nombre}",
#         },
#     )


# @login_required
# @require_POST
# def proveedor_eliminar(request, pk):
#     item = get_object_or_404(Proveedor, pk=pk)
#     item.delete()
#     return HttpResponse(
#         status=204,
#         headers={
#             "HX-Trigger": json.dumps(
#                 {
#                     "showMessage": f"{item.nombre} eliminado.",
#                 }
#             )
#         },
#     )
