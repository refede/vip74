# my_app/management/commands/import_materias.py
import csv
import os
from decimal import Decimal, InvalidOperation
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.conf import settings

# Asegúrate de que la ruta a tus modelos sea correcta
from inspeccion.models import (Instructivo, Metodo, InstructivoMetodo)

# --- DEFINE LA RUTA A TU CSV AQUÍ ---
CSV_PATH = "D:/Users/rflores/Documents/@Refede/Code/db/csv/inspeccion_instructivometodo.csv"
# -----------------------------------------

class Command(BaseCommand):
    help = "Importa NUEVAS elementos desde un CSV (ruta hardcodeada) usando bulk_create."

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
            help="Si se especifica, ignora filas que causarían conflictos de unicidad (id).",
        )
        # Podrías añadir una opción para ignorar materias si su categoría no se encuentra

    def _cast_to_decimal(self, value_str, field_name, line_num, default=None):
        if value_str is None or str(value_str).strip() == "":
            return default
        try:
            return Decimal(value_str)
        except InvalidOperation:
            self.stderr.write(
                self.style.WARNING(
                    f"Línea {line_num}: Valor decimal inválido '{value_str}' para '{field_name}'. Se usará {default}."
                )
            )
            return default

    def _cast_to_int(self, value_str, field_name, line_num, default=0):
        if value_str is None or str(value_str).strip() == "":
            return default
        try:
            return int(float(value_str))
        except ValueError:
            self.stderr.write(
                self.style.WARNING(
                    f"Línea {line_num}: Valor entero inválido '{value_str}' para '{field_name}'. Se usará {default}."
                )
            )
            return default

    def _parse_boolean(self, value_str):
        """Convierte strings a booleano de forma flexible."""
        value_str_lower = str(value_str).lower().strip()
        if value_str_lower in ("true", "t", "1", "yes", "y", "si", "sí", 1):
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
                f"Iniciando importación BULK para Materia desde: {csv_file_path}"
            )
        )

        # Paso 1: Cargar fk en caché
        self.stdout.write("Cargando FK en caché...")
        fk_cache_1 = {foreign.id: foreign for foreign in Instructivo.objects.all()}
        # print(fk_cache)
        if not fk_cache_1:
            self.stdout.write(
                self.style.WARNING(
                    "No hay FK en la base de datos. ¿Se importaron primero?"
                )
            )
            # Podrías decidir detenerte aquí si las categorías son obligatorias
        self.stdout.write(f"Cargadas {len(fk_cache_1)} fks en caché.")

        fk_cache_2 = {foreign.id: foreign for foreign in Metodo.objects.all()}
        # print(fk_cache)
        if not fk_cache_2:
            self.stdout.write(
                self.style.WARNING(
                    "No hay FK en la base de datos. ¿Se importaron primero?"
                )
            )
            # Podrías decidir detenerte aquí si las categorías son obligatorias
        self.stdout.write(f"Cargadas {len(fk_cache_2)} fks en caché.")

        elementos_a_crear = []
        errores_filas = []

        try:
            with open(csv_file_path, mode="r", encoding="utf-8-sig") as csvfile:
                reader = csv.DictReader(csvfile)
                for i, row in enumerate(reader):
                    line_num = i + 2

                    id              = row.get("id")
                    fk_instructivo  = row.get("instructivo_id")
                    orden           = row.get("orden")
                    fk_metodo       = row.get("metodo_id")
                    critico         = row.get("critico")
                    requerido       = row.get("requerido")
                    estado          = row.get("estado")
                    obs             = row.get("obs")

                    if not id :
                        errores_filas.append(
                            f"Línea {line_num}: 'id' es obligatorio."
                        )
                        continue

                    if not fk_instructivo or not fk_metodo:
                        errores_filas.append(
                            f"Línea {line_num} (ID: {fk_instructivo} {fk_metodo}): 'fk' es obligatorio."
                        )
                        continue

                    fk_instructivo_obj = fk_cache_1.get((str(fk_instructivo)))

                    if not fk_instructivo_obj:
                        errores_filas.append(
                            f"Línea {line_num} (ID: {fk_instructivo}): FK de elemento no encontrada en la base de datos. Será omitida.")
                        continue

                    fk_metodo_obj = fk_cache_2.get((str(fk_metodo)))

                    if not fk_metodo_obj:
                        errores_filas.append(
                            f"Línea {line_num} (ID: {fk_metodo}): FK de elemento no encontrada en la base de datos. Será omitida.")
                        continue

                    elemento_instance = InstructivoMetodo(
                        id              =id,
                        instructivo     =fk_instructivo_obj,
                        orden           =orden,
                        metodo          =fk_metodo_obj,
                        critico         =critico,
                        requerido       =requerido,
                        estado          =estado,
                        obs             =obs
                    )
                    elementos_a_crear.append(elemento_instance)

        except Exception as e:
            raise CommandError(f"Error leyendo CSV: {e}")

        if errores_filas:
            self.stderr.write(
                self.style.WARNING(
                    f"Se encontraron {len(errores_filas)} errores en filas del CSV:"
                )
            )
            for error in errores_filas[:10]:
                self.stderr.write(f"- {error}")
            if len(errores_filas) > 10:
                self.stderr.write(f"- ... y {len(errores_filas) - 10} más.")

        if not elementos_a_crear:
            self.stdout.write(self.style.WARNING("No hay elementos válidas para crear."))
            return

        self.stdout.write(
            f"Preparando para crear {len(elementos_a_crear)} elementos en lotes de {batch_size}..."
        )
        try:
            with transaction.atomic():
                created_objects = InstructivoMetodo.objects.bulk_create(
                    elementos_a_crear,
                    batch_size=batch_size,
                    ignore_conflicts=ignore_conflicts,
                )

            num_creados = len(created_objects)
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
                self.style.ERROR(f"Error durante bulk_create: {e}")
            )
            raise CommandError(
                f"Fallo en la operación de bulk_create: {e}"
            )
