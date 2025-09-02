import csv
import json

from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction
from django.http import JsonResponse, HttpResponse, HttpResponseServerError
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
                headers={
                    "HX-Trigger": json.dumps(
                        {"showMessage": f"{categoria.nombre} creado."}
                    )
                },
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

    return render(
        request,
        "almacen/categoria_materia_form.html",
        {
            "form": form,
            "item": item,
            "titulo": f"{item.nombre}",
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
    # 1. Obtener todas las materias y pre-cargar sus características y el nombre de la característica
    #    Esto hace solo 3 consultas a la BBDD, sin importar cuántas materias tengas. ¡Muy eficiente!
    materias_qs = Materia.objects.all().prefetch_related(
        'valores_caracteristicas__caracteristica',
        'propiedades_especificas__propiedad',
    )
    # 2. Construir la lista de datos a mano
    materias = []
    for materia in materias_qs:
        # Creamos un diccionario base con los datos directos de la materia
        materia_data = {
            "id":                   materia.id,
            "nombre":               materia.nombre,
            "categoria__nombre":    materia.categoria.abreviatura,
            "costo":                materia.costo,
            "date_updated":         materia.date_updated,
            "estado":               materia.estado,
            # características
            "tipo":                 None,
            "estructura":          None,
            # especificaciones <- propiedades
            "espesor":              None,
            "ancho":                None,
            "peso lineal":          None,
        }

        # 3. Iterar sobre las especificaciones pre-cargadas (esto ya no consulta la BBDD)
        for especificacion in materia.propiedades_especificas.all():
            # El nombre de la propiedad está en especificacion.propiedad.nombre
            nombre_propiedad = especificacion.propiedad.nombre.lower()
            
            # Si encontramos una de las propiedades que buscamos, la añadimos al diccionario.
            # El valor es un DecimalField, por lo que no necesita conversión.
            if nombre_propiedad == 'espesor':
                materia_data['espesor'] = especificacion.valor
            elif nombre_propiedad == 'peso lineal':
                materia_data['peso lineal'] = especificacion.valor
            elif nombre_propiedad == 'ancho':
                materia_data['ancho'] = especificacion.valor

        for caracteristica in materia.valores_caracteristicas.all():
            # El nombre de la propiedad está en especificacion.propiedad.nombre
            nombre_caracteristica = caracteristica.caracteristica.nombre.lower()
            
            # Si encontramos una de las propiedades que buscamos, la añadimos al diccionario.
            # El valor es un DecimalField, por lo que no necesita conversión.
            if nombre_caracteristica == 'tipo':
                materia_data['tipo'] = caracteristica.valor
            elif nombre_caracteristica == 'estructura':
                materia_data['estructura'] = caracteristica.valor
        materias.append(materia_data)
        # print(materias)
    return JsonResponse({"data": materias})


@login_required
def materia_crear(request):
    if request.method == "POST":
        form = MateriaForm(request.POST)
        if form.is_valid():
            materia = form.save()
            # Ahora, iteramos sobre los datos del POST para encontrar nuestras características
            for key, value in request.POST.items():
                if key.startswith("caracteristica_"):
                    # Si el input se llama 'caracteristica_5', el id es 5
                    caracteristica_id = int(key.split("_")[1])
                    # Si el usuario ha introducido un valor
                    if value:
                        # Creamos o actualizamos el objeto ValorCaracteristicaMateria
                        CaracteristicaMateria.objects.update_or_create(
                            materia=materia,
                            caracteristica_id=caracteristica_id,
                            defaults={"valor": value},
                        )
                if key.startswith("propiedad_"):
                    propiedad_id = int(key.split("_")[1])
                    # Si el usuario ha introducido un valor
                    if value:
                        # Creamos o actualizamos el objeto ValorCaracteristicaMateria
                        EspecificacionMateria.objects.update_or_create(
                            materia=materia,
                            propiedad_id=propiedad_id,
                            defaults={"valor": value},
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
        # try:
        form = MateriaForm(request.POST, instance=item)
        if form.is_valid():
            materia = form.save()  # Guardamos los cambios principales de Materia
            # --- LÓGICA DE GUARDADO DE CARACTERÍSTICAS Y ESPECIFICACIONES ---
            for key, value in request.POST.items():
                # Manejo de Características
                if key.startswith("caracteristica_"):
                    caracteristica_id = int(key.split("_")[1])
                    if value:  # Si hay un valor, crear o actualizar
                        CaracteristicaMateria.objects.update_or_create(
                            materia=materia,
                            caracteristica_id=caracteristica_id,
                            defaults={"valor": value.strip()},
                        )
                    else:  # Si el valor está vacío, eliminar la relación si existe
                        CaracteristicaMateria.objects.filter(
                            materia=materia, caracteristica_id=caracteristica_id
                        ).delete()
                # Manejo de Especificaciones (Propiedades)
                if key.startswith("propiedad_"):
                    propiedad_id = int(key.split("_")[1])
                    if value:  # Si hay un valor, crear o actualizar
                        EspecificacionMateria.objects.update_or_create(
                            materia=materia,
                            propiedad_id=propiedad_id,
                            defaults={"valor": value},
                        )
                    else:  # Si el valor está vacío, eliminar la relación si existe
                        EspecificacionMateria.objects.filter(
                            materia=materia, propiedad_id=propiedad_id
                        ).delete()
            # Respuesta de éxito para HTMX
            return HttpResponse(
                status=204,
                headers={
                    "HX-Trigger": json.dumps(
                        {"showMessage": f"{item.nombre} editado."}
                    )
                },
            )
    else:  # Si es un método GET
        form = MateriaForm(instance=item)

    # --- LÓGICA DE PREPARACIÓN DEL CONTEXTO (Se ejecuta para GET y para POST inválido) ---
    # 1. Obtener plantillas desde la categoría
    caracteristicas_plantilla = item.categoria.caracteristicas.all()
    especificaciones_plantilla = item.categoria.especificaciones.all()
    # 2. Obtener valores ya guardados para esta materia en diccionarios
    valores_caracteristicas = {
        vc.caracteristica_id: vc.valor for vc in item.valores_caracteristicas.all()
    }
    valores_especificaciones = {
        es.propiedad_id: es.valor for es in item.propiedades_especificas.all()
    }
    # 3. "Hidratar" las plantillas con los valores guardados
    caracteristicas_con_valores = []
    for c in caracteristicas_plantilla:
        c.valor_actual = valores_caracteristicas.get(c.id, "")
        caracteristicas_con_valores.append(c)
    especificaciones_con_valores = []
    for e in especificaciones_plantilla:
        e.valor_actual = valores_especificaciones.get(e.id)
        especificaciones_con_valores.append(e)
    # 4. Construir el contexto final COMPLETO
    context = {
        "form": form,
        "item": item,
        "object": item,
        "titulo": f"{item.nombre}",
        "caracteristicas": caracteristicas_con_valores,
        "especificaciones": especificaciones_con_valores,
    }
    # 5. Renderizar la plantilla con el contexto completo
    return render(request, "almacen/materia_form.html", context)


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
            nuevo_id = form.cleaned_data["nuevo_id"]
            
            # 1. Verificación de unicidad del nuevo ID
            if Materia.objects.filter(id=nuevo_id).exists():
                form.add_error("nuevo_id", "El código ya existe.")
                return render(
                    request,
                    "almacen/materia_clonar_form.html",
                    {
                        "form": form,
                        "titulo": f"Clonar {objeto_a_clonar}",
                    },
                )
            
            # 2. Iniciar una transacción para garantizar "todo o nada"
            try:
                with transaction.atomic():
                    # 2.1. Crear y guardar la nueva Materia (el objeto "padre")
                    objeto_nuevo = Materia(
                        id=nuevo_id,
                        nombre=f"{objeto_a_clonar.nombre} (Clonado)", # Mejorado: clonar el nombre
                        categoria=objeto_a_clonar.categoria,
                        costo=objeto_a_clonar.costo,
                        estado=objeto_a_clonar.estado,
                        obs=objeto_a_clonar.obs,
                    )
                    objeto_nuevo.save()

                    # 2.2. Clonar las Características relacionadas
                    caracteristicas_originales = objeto_a_clonar.valores_caracteristicas.all()
                    nuevas_caracteristicas = []
                    for carac_original in caracteristicas_originales:
                        nuevas_caracteristicas.append(
                            CaracteristicaMateria(
                                materia=objeto_nuevo,
                                caracteristica=carac_original.caracteristica,
                                valor=carac_original.valor
                            )
                        )
                    
                    if nuevas_caracteristicas:
                        CaracteristicaMateria.objects.bulk_create(nuevas_caracteristicas)

                    # 2.3. Clonar las Especificaciones relacionadas
                    especificaciones_originales = objeto_a_clonar.propiedades_especificas.all()
                    nuevas_especificaciones = []
                    for espec_original in especificaciones_originales:
                        nuevas_especificaciones.append(
                            EspecificacionMateria(
                                materia=objeto_nuevo,
                                propiedad=espec_original.propiedad,
                                valor=espec_original.valor
                            )
                        )

                    if nuevas_especificaciones:
                        EspecificacionMateria.objects.bulk_create(nuevas_especificaciones)

            except Exception as e:
                # Si algo falla dentro de la transacción, se revierte todo.
                # Aquí puedes manejar el error, por ejemplo, mostrándolo al usuario.
                # (Para simplificar, por ahora solo lo registramos o lo ignoramos)
                # logger.error(f"Error al clonar materia: {e}")
                form.add_error(None, f"Ocurrió un error inesperado durante la clonación: {e}")
                return render(
                    request,
                    "almacen/materia_clonar_form.html",
                    {
                        "form": form,
                        "titulo": f"Clonar {objeto_a_clonar}",
                    },
                )

            # 3. Si todo salió bien, enviar la respuesta de éxito
            return HttpResponse(
                status=204,
                headers={
                    "HX-Trigger": json.dumps({
                        "showMessage": f"Objeto {objeto_a_clonar.id} clonado a {nuevo_id} exitosamente."
                    })
                },
            )

    else: # Método GET
        form = MateriaClonarForm()

    # Contexto para la petición GET y para cuando el formulario es inválido
    context = {
        "form": form,
        "titulo": f"Clonar {objeto_a_clonar}",
    }
    return render(request, "almacen/materia_clonar_form.html", context)


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


@login_required
def materia_detalles_categoria(request):
    """
    Vista llamada por HTMX cuando cambia la categoría.
    Devuelve un fragmento HTML que contiene los campos tanto para
    características como para especificaciones.
    """
    categoria_id = request.GET.get("categoria")
    materia_id = request.GET.get("materia_id")  # Para el caso de edición

    if not categoria_id:
        return HttpResponse("")

    try:
        categoria = CategoriaMateria.objects.get(pk=categoria_id)
    except CategoriaMateria.DoesNotExist:
        return HttpResponse("")

    caracteristicas = categoria.caracteristicas.all()
    especificaciones = categoria.especificaciones.all()

    # Si estamos editando una materia, obtenemos sus valores actuales
    if materia_id:
        try:
            materia = Materia.objects.get(pk=materia_id)

            # Cargar valores de características
            valores_caracteristicas = {
                vc.caracteristica_id: vc.valor
                for vc in materia.valores_caracteristicas.all()
            }
            for c in caracteristicas:
                c.valor_actual = valores_caracteristicas.get(c.id, "")

            # Cargar valores de especificaciones (¡CORRECCIÓN IMPORTANTE!)
            # El related_name es 'propiedades_especificas' y el FK es 'propiedad'
            valores_especificaciones = {
                es.propiedad_id: es.valor
                for es in materia.propiedades_especificas.all()
            }
            for e in especificaciones:
                e.valor_actual = valores_especificaciones.get(e.id, None)

        except Materia.DoesNotExist:
            # Si la materia no existe, no hacemos nada con los valores
            pass

    context = {"caracteristicas": caracteristicas, "especificaciones": especificaciones}
    # Renderizamos un nuevo template "wrapper" que incluye los otros dos
    return render(request, "almacen/partials/materia_detalles_categoria.html", context)


def materia_caracteristicas(request):
    """
    Vista llamada por HTMX cuando el usuario selecciona una categoría
    en el formulario de Materia. Devuelve los campos de input para
    las características de esa categoría.
    """
    categoria_id = request.GET.get("categoria")
    materia_id = request.GET.get("materia_id")  # Para el caso de edición

    if not categoria_id:
        return HttpResponse("")

    categoria = CategoriaMateria.objects.get(pk=categoria_id)
    caracteristicas = categoria.caracteristicas.all()  # O 'caracteristicas_plantilla'

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

    context = {"caracteristicas": caracteristicas}
    return render(
        request, "almacen/partials/materia_caracteristicas_valores.html", context
    )


def materia_especificaciones(request):
    """
    analogos al anterior
    """
    categoria_id = request.GET.get("categoria")
    materia_id = request.GET.get("materia_id")  # Para el caso de edición

    if not categoria_id:
        return HttpResponse("")

    categoria = CategoriaMateria.objects.get(pk=categoria_id)
    especificaciones = categoria.especificaciones.all()  # O 'caracteristicas_plantilla'

    # Si estamos editando una materia, necesitamos obtener sus valores actuales
    if materia_id:
        materia = Materia.objects.get(pk=materia_id)
        valores_actuales = {
            vc.especificaciones_id: vc.valor
            for vc in materia.valores_especificaciones.all()
        }
        # Añadimos el valor actual a cada característica para pasarlo a la plantilla
        for c in especificaciones:
            c.valor_actual = valores_actuales.get(c.id)

    context = {"especificaciones": especificaciones}
    return render(
        request, "almacen/partials/materia_especificaciones_valores.html", context
    )


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
