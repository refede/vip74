from django.contrib import admin
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ManyToManyWidget
from .models import Caracteristica, CategoriaMateria, Materia
from .resources import CategoriaMateriaResource, MateriaResource
from inspeccion.models import Propiedad


@admin.register(Materia)
class MateriaAdmin(ImportExportModelAdmin):
    # Le decimos al admin que use la clase que hemos importado.
    # El resto de su comportamiento no cambia.
    resource_class = MateriaResource
    
    list_display = ('id', 'nombre', 'categoria', 'costo', 'estado')
    search_fields = ('id', 'nombre', 'categoria__nombre')
    list_filter = ('categoria', 'estado')

    # Este método sigue siendo importante para la eficiencia de la exportación.
    def get_export_queryset(self, request):
        return super().get_export_queryset(request).prefetch_related(
            'valores_caracteristicas__caracteristica',
            'propiedades_especificas__propiedad'
        )


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