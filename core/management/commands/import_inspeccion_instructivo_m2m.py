# my_app/management/commands/import_categorias_materia.py
import csv
import os
from datetime import datetime
from decimal import Decimal, InvalidOperation
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
# from django.conf import settings
from user.models import Persona  # CAMBIA 'tu_app' por el nombre de tu app
from inspeccion.models import Instructivo  # CAMBIA 'tu_app' por el nombre de tu app

# --- DEFINE LA RUTA A TU CSV AQUÍ ---
CSV_PATH = "D:/Users/rflores/Documents/@Refede/Code/db/csv/inspeccion_instructivo.csv"
# -----------------------------------------


class Command(BaseCommand):
    help = "Importa NUEVAS Categorías de Materia desde un CSV (ruta hardcodeada) usando bulk_create."

    def add_arguments(self, parser):
        parser.add_argument(
            "--batch-size",
            type=int,
            default=500,
            help="Número de objetos a crear en cada consulta bulk.",
        )
        parser.add_argument(
            "--ignore-conflicts",
            action="store_true",
            help="Si se especifica, ignora filas que causarían conflictos de unicidad (nombre, abreviatura).",
        )

    def _cast_to_date(
        self, date_str, field_name, line_num, default=None, date_format="%Y-%m-%d"
    ):
        if date_str is None or str(date_str).strip() == "":
            return default
        try:
            return datetime.strptime(date_str, date_format).date()
        except ValueError:
            self.stderr.write(
                self.style.WARNING(
                    f"Línea {line_num}: Fecha inválida '{date_str}' para '{field_name}'. Se usará {default}."
                )
            )
            return default

    def _parse_boolean(self, value_str):
        """Convierte strings a booleano de forma flexible."""
        value_str_lower = str(value_str).lower().strip()
        if value_str_lower in ("true", "t", "1", "yes", "y", "si", "sí"):
            return True
        if value_str_lower in ("false", "f", "0", "no", "n"):
            return False
        # Podrías levantar un error o retornar un default si el valor no es reconocido
        self.stderr.write(
            self.style.WARNING(
                f"Valor booleano no reconocido '{value_str}', se asume False."
            )
        )
        return False

    def handle(self, *args, **options):
        csv_file_path = CSV_PATH
        batch_size = options["batch_size"]
        ignore_conflicts = options["ignore_conflicts"]

        if not os.path.exists(csv_file_path):
            raise CommandError(f"Archivo CSV no encontrado: {csv_file_path}")

        self.stdout.write(
            self.style.SUCCESS(
                f"Iniciando importación BULK para CategoriaMateria desde: {csv_file_path}"
            )
        )

        # Paso 1: Cargar fk en caché
        self.stdout.write("Cargando FK en caché...")
        fk_cache = {foreign.id: foreign for foreign in Persona.objects.all()}
        print(fk_cache)
        if not fk_cache:
            self.stdout.write(
                self.style.WARNING(
                    "No hay FK en la base de datos. ¿Se importaron primero?"
                )
            )
            # Podrías decidir detenerte aquí si las categorías son obligatorias
        self.stdout.write(f"Cargadas {len(fk_cache)} fks en caché.")

        elementos_a_crear = []
        errores_filas = []

        try:
            with open(csv_file_path, mode="r", encoding="utf-8-sig") as csvfile:
                reader = csv.DictReader(csvfile)
                for i, row in enumerate(reader):
                    line_num = i + 2  # +1 por encabezado, +1 por 0-indexed

                    id          = row.get("id")
                    nombre      = row.get("nombre")
                    version     = row.get("version")
                    objetivo    = row.get("objetivo")
                    registro    = row.get("registro")
                    fk_1        = row.get("elabora_id")
                    fk_2        = row.get("revisa_id")
                    fk_3        = row.get("aprueba_id")
                    aprobacion  = row.get("aprobacion")
                    estado      = row.get('estado')
                    obs         = row.get("obs")

                    if not nombre or not estado:
                        errores_filas.append(
                            f"Línea {line_num}: 'nombre' y 'estado' son obligatorios."
                        )
                        continue

                    fk_obj_1 = fk_cache.get(int(str(fk_1).strip()))
                    fk_obj_2 = fk_cache.get(int(str(fk_2).strip()))
                    fk_obj_3 = fk_cache.get(int(str(fk_3).strip()))

                    if not fk_obj_1 or not fk_obj_2 or not fk_obj_3:
                        errores_filas.append(
                            f"Línea {line_num} (ID: {id}): FK de elemento '{fk_obj_1}' '{fk_obj_2}' '{fk_obj_3}' no encontrada en la base de datos. Este elemento será omitida."
                        )
                        continue

                    modelo_instance = Instructivo(
                        id         = id,
                        nombre     = nombre,
                        version    = version,
                        objetivo   = objetivo,
                        registro   = registro,
                        elabora    = fk_obj_1,
                        revisa     = fk_obj_2,
                        aprueba    = fk_obj_3,
                        aprobacion = self._cast_to_date(aprobacion, "aprobacion", line_num),
                        estado     = estado,
                        obs        = obs,
                    )
                    elementos_a_crear.append(modelo_instance)

        except Exception as e:
            raise CommandError(f"Error leyendo CSV: {e}")

        if errores_filas:
            self.stderr.write(
                self.style.WARNING(
                    f"Se encontraron {len(errores_filas)} errores en filas del CSV de Categorías:"
                )
            )
            for error in errores_filas[:10]:
                self.stderr.write(f"- {error}")
            if len(errores_filas) > 10:
                self.stderr.write(f"- ... y {len(errores_filas) - 10} más.")

        if not elementos_a_crear:
            self.stdout.write(
                self.style.WARNING("No hay elementos válidos para crear.")
            )
            return

        self.stdout.write(
            f"Preparando para crear {len(elementos_a_crear)} elementos en lotes de {batch_size}..."
        )
        try:
            with transaction.atomic():
                created_objects = Instructivo.objects.bulk_create(
                    elementos_a_crear,
                    batch_size=batch_size,
                    ignore_conflicts=ignore_conflicts,
                )

            num_creados = len(created_objects)
            # Con ignore_conflicts=True, Django no establece los PKs en los objetos de la lista si hubo conflictos.
            # created_objects contendrá solo los que se insertaron.
            self.stdout.write(
                self.style.SUCCESS(
                    f"¡Importación BULK de elementos completada! Se crearon {num_creados} elementos."
                )
            )
            if ignore_conflicts and num_creados < len(elementos_a_crear):
                self.stdout.write(
                    self.style.WARNING(
                        f"Se intentaron procesar {len(elementos_a_crear)} elementos, pero solo {num_creados} fueron creadas (las demás probablemente ya existían y fueron ignoradas)."
                    )
                )

        except Exception as e:
            self.stderr.write(
                self.style.ERROR(f"Error durante bulk_create para Modelo: {e}")
            )
            raise CommandError(f"Fallo en la operación de bulk_create para Modelo: {e}")
