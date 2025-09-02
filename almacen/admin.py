from django.contrib import admin
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ManyToManyWidget
from .models import Caracteristica, CategoriaMateria, Materia
from inspeccion.models import Propiedad


# Definir el recurso para importar/exportar
class CategoriaMateriaResource(resources.ModelResource):
    # Declaramos explícitamente el campo 'caracteristicas'.
    # Esto sobreescribe el comportamiento por defecto.
    caracteristicas = fields.Field(
        attribute='caracteristicas',  # El atributo en el modelo CategoriaMateria
        widget=ManyToManyWidget(
            model=Caracteristica,   # El modelo relacionado
            field='nombre',         # El campo del modelo relacionado que se usará para buscar y mostrar
            separator='|'           # El carácter que unirá/separará los múltiples valores
        )
    )

    # Hacemos lo mismo para el campo 'especificaciones'.
    especificaciones = fields.Field(
        attribute='especificaciones',
        widget=ManyToManyWidget(
            model=Propiedad,        # El modelo relacionado
            field='nombre',         # Asumo que Propiedad tiene un campo 'nombre' que es único o representativo
            separator='|'
        )
    )
    class Meta:
        model = CategoriaMateria
        fields = (
            "id",
            "nombre",
            "abreviatura",
            "bloque",
            "caracteristicas",
            "especificaciones",
        )  # campos a incluir
        # export_order = ("id", "nombre", "descripcion")


@admin.register(CategoriaMateria)
class CategoriaMateriaAdmin(ImportExportModelAdmin):
    resource_class = CategoriaMateriaResource
    list_display = (
        "id",
        "nombre",
        "abreviatura",
        "bloque",
        "mostrar_caracteristicas",  # Nombre del método
        "mostrar_especificaciones",  # Nombre del método
    )
    # Para mejorar el rendimiento, usamos prefetch_related
    # Esto le dice a Django que obtenga todos los objetos relacionados en una sola consulta extra
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.prefetch_related('caracteristicas', 'especificaciones')
        return queryset

    # --- MÉTODO PARA CARACTERÍSTICAS ---
    def mostrar_caracteristicas(self, obj):
        """
        Crea una cadena de texto con los nombres de las características,
        separados por una coma y un espacio.
        """
        # obj.caracteristicas.all() ya está pre-cargado gracias a prefetch_related
        return ", ".join([c.nombre for c in obj.caracteristicas.all()])
    
    # Le damos un nombre corto para que se vea bien en la cabecera de la tabla
    mostrar_caracteristicas.short_description = "Características"

    # --- MÉTODO PARA ESPECIFICACIONES ---
    def mostrar_especificaciones(self, obj):
        """
        Crea una cadena de texto con los nombres de las especificaciones.
        Asumimos que el modelo Propiedad tiene un campo 'nombre'. 
        Ajusta 'p.nombre' si el campo se llama de otra manera.
        """
        return ", ".join([p.nombre for p in obj.especificaciones.all()])

    # Le damos un nombre corto para la cabecera
    mostrar_especificaciones.short_description = "Especificaciones"

    # BONUS: Habilitar el filtrado, que SÍ funciona bien con ManyToManyField
    list_filter = ('bloque', 'caracteristicas', 'especificaciones')
    
    # BONUS: Búsqueda en campos relacionados (¡muy útil!)
    search_fields = ('nombre', 'abreviatura', 'caracteristicas__nombre', 'especificaciones__nombre')