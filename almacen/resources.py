from import_export import resources, fields
from import_export.results import RowResult
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget
from .models import (
    Materia,
    CategoriaMateria,
    Caracteristica,
    CaracteristicaMateria,
    EspecificacionMateria,
)
from inspeccion.models import (
    Propiedad,
)  # Asegúrate de que esta importación sea correcta


class CategoriaMateriaResource(resources.ModelResource):
    # Declaramos explícitamente el campo 'caracteristicas'.
    # Esto sobreescribe el comportamiento por defecto.
    caracteristicas = fields.Field(
        attribute="caracteristicas",  # El atributo en el modelo CategoriaMateria
        widget=ManyToManyWidget(
            model=Caracteristica,  # El modelo relacionado
            field="nombre",  # El campo del modelo relacionado que se usará para buscar y mostrar
            separator="|",  # El carácter que unirá/separará los múltiples valores
        ),
    )

    # Hacemos lo mismo para el campo 'especificaciones'.
    especificaciones = fields.Field(
        attribute="especificaciones",
        widget=ManyToManyWidget(
            model=Propiedad,  # El modelo relacionado
            field="nombre",  # Asumo que Propiedad tiene un campo 'nombre' que es único o representativo
            separator="|",
        ),
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


class MateriaResource(resources.ModelResource):
    categoria = fields.Field(
        attribute="categoria",
        widget=ForeignKeyWidget(CategoriaMateria, "nombre"),
    )

    class Meta:
        model = Materia
        fields = ("id", "nombre", "categoria", "costo", "estado")
        import_id_fields = ("id",)
        skip_unchanged = True
        report_skipped = False

    def __init__(self, *args, **kwargs):
        """
        Al iniciar el Resource, agregamos dinámicamente un field
        para cada característica y especificación existente.
        """
        super().__init__(*args, **kwargs)

        # --- Características dinámicas ---
        for c in Caracteristica.objects.all():
            col_name = f"caracteristica_{c.nombre}"
            self.fields[col_name] = fields.Field(column_name=col_name)

        # --- Especificaciones dinámicas ---
        for p in Propiedad.objects.all():
            col_name = f"especificacion_{p.nombre}"
            self.fields[col_name] = fields.Field(column_name=col_name)

    # -------------------------------
    # EXPORTACIÓN
    # -------------------------------
    def export_field(self, field, obj, **kwargs):
        """
        Devuelve valores dinámicos para características/especificaciones.
        """
        if field.column_name in ("id", "nombre", "categoria", "costo", "estado"):
            return super().export_field(field, obj, **kwargs)

        # Características
        if field.column_name.startswith("caracteristica_"):
            nombre_caract = field.column_name[len("caracteristica_") :]
            valor = (
                obj.valores_caracteristicas.filter(
                    caracteristica__nombre=nombre_caract
                ).first()
            )
            return valor.valor if valor else ""

        # Especificaciones
        if field.column_name.startswith("especificacion_"):
            nombre_prop = field.column_name[len("especificacion_") :]
            valor = (
                obj.propiedades_especificas.filter(
                    propiedad__nombre=nombre_prop
                ).first()
            )
            return valor.valor if valor else ""

        return ""

    # -------------------------------
    # IMPORTACIÓN
    # -------------------------------
    def import_obj(self, obj, data, dry_run):
        """
        Procesa también las columnas dinámicas al importar.
        """
        super().import_obj(obj, data, dry_run)

        if dry_run:
            return

        obj.save()  # Necesario para tener el `id` disponible

        # --- Procesar características ---
        for c in Caracteristica.objects.all():
            col = f"caracteristica_{c.nombre}"
            valor = data.get(col)
            if valor not in [None, ""]:
                CaracteristicaMateria.objects.update_or_create(
                    materia=obj,
                    caracteristica=c,
                    defaults={"valor": str(valor)},
                )

        # --- Procesar especificaciones ---
        for p in Propiedad.objects.all():
            col = f"especificacion_{p.nombre}"
            valor = data.get(col)
            if valor not in [None, ""]:
                EspecificacionMateria.objects.update_or_create(
                    materia=obj,
                    propiedad=p,
                    defaults={"valor": valor},
                )

