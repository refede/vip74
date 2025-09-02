from import_export import resources, fields
from import_export.results import RowResult
from import_export.widgets import ForeignKeyWidget
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


class MateriaResource(resources.ModelResource):
    categoria = fields.Field(
        attribute="categoria",
        widget=ForeignKeyWidget(model=CategoriaMateria, field="nombre"),
    )

    class Meta:
        model = Materia
        fields = ("id", "nombre", "categoria", "costo", "estado")
        import_id_fields = ("id",)
        skip_unchanged = True
        report_skipped = False

    def after_import_row(self, row, row_result, **kwargs):
        # Solo procedemos si la fila resultó en una creación o actualización exitosa.
        if row_result.import_type in [
            RowResult.IMPORT_TYPE_NEW,
            RowResult.IMPORT_TYPE_UPDATE,
        ]:
            # Obtenemos el ID del objeto Materia recién guardado. Esta es la forma más segura.
            materia_id = row_result.object_id

            # --- PROCESAR CARACTERÍSTICAS DINÁMICAS ---
            caracteristica_prefix = "caracteristica_"
            for col_name, valor in row.items():
                if col_name is not None and col_name.startswith(caracteristica_prefix):
                    if valor is None or str(valor).strip() == "":
                        continue

                    nombre_caracteristica = col_name[len(caracteristica_prefix) :]
                    try:
                        caracteristica_obj = Caracteristica.objects.get(
                            nombre=nombre_caracteristica
                        )

                        # --- CAMBIO CLAVE ---
                        # Usamos el ID directamente en lugar del objeto instancia.
                        CaracteristicaMateria.objects.update_or_create(
                            materia_id=materia_id,
                            caracteristica=caracteristica_obj,
                            defaults={"valor": str(valor)},
                        )
                    except Caracteristica.DoesNotExist:
                        pass

            # --- PROCESAR ESPECIFICACIONES DINÁMICAS ---
            especificacion_prefix = "especificacion_"
            for col_name, valor in row.items():
                if col_name is not None and col_name.startswith(especificacion_prefix):
                    if valor is None or str(valor).strip() == "":
                        continue

                    nombre_propiedad = col_name[len(especificacion_prefix) :]
                    try:
                        propiedad_obj = Propiedad.objects.get(nombre=nombre_propiedad)

                        # --- CAMBIO CLAVE ---
                        # Usamos el ID directamente en lugar del objeto instancia.
                        EspecificacionMateria.objects.update_or_create(
                            materia_id=materia_id,
                            propiedad=propiedad_obj,
                            defaults={"valor": valor},
                        )
                    except Propiedad.DoesNotExist:
                        pass
