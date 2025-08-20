# my_app/management/commands/import_materias.py
import csv
import os
from decimal import Decimal, InvalidOperation
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.conf import settings

# Asegúrate de que la ruta a tus modelos sea correcta
from almacen.models import (
    Materia,
    CategoriaMateria,
)  # CAMBIA 'tu_app' por el nombre de tu app

# --- DEFINE LA RUTA A TU CSV AQUÍ ---
# CSV_MATERIAS_PATH = os.path.join(settings.BASE_DIR, "data", "Materia.csv")
CSV_MATERIAS_PATH = "D:/Users/rflores/Documents/@Refede/Code/db/csv/materias_materia.csv"

# -----------------------------------------


class Command(BaseCommand):
    help = "Importa NUEVAS Materias desde un CSV (ruta hardcodeada) usando bulk_create."

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
            help="Si se especifica, ignora filas de Materia que causarían conflictos de unicidad (id).",
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

    def handle(self, *args, **options):
        csv_file_path = CSV_MATERIAS_PATH
        batch_size = options["batch_size"]
        ignore_conflicts = options["ignore_conflicts"]

        if not os.path.exists(csv_file_path):
            raise CommandError(f"Archivo CSV no encontrado: {csv_file_path}")

        self.stdout.write(
            self.style.SUCCESS(
                f"Iniciando importación BULK para Materia desde: {csv_file_path}"
            )
        )

        # Paso 1: Cargar Categorías de Materia en caché
        self.stdout.write("Cargando Categorías de Materia en caché...")
        categorias_cache = {cat.id: cat for cat in CategoriaMateria.objects.all()}
        # print(categorias_cache)
        if not categorias_cache:
            self.stdout.write(
                self.style.WARNING(
                    "No hay Categorías de Materia en la base de datos. ¿Se importaron primero?"
                )
            )
            # Podrías decidir detenerte aquí si las categorías son obligatorias
        self.stdout.write(f"Cargadas {len(categorias_cache)} categorías en caché.")

        materias_a_crear = []
        errores_filas = []

        try:
            with open(csv_file_path, mode="r", encoding="utf-8-sig") as csvfile:
                reader = csv.DictReader(csvfile)
                for i, row in enumerate(reader):
                    line_num = i + 2

                    materia_id = row.get("mp_codigo")
                    nombre_materia = row.get("mp_nombre")
                    categoria_nombre_csv = row.get("mp_categoria_link_id")
                    # print(categoria_nombre_csv)

                    if not materia_id or not nombre_materia:
                        errores_filas.append(
                            f"Línea {line_num}: 'id' y 'nombre' de Materia son obligatorios."
                        )
                        continue

                    if not categoria_nombre_csv:
                        errores_filas.append(
                            f"Línea {line_num} (ID: {materia_id}): 'categoria_nombre' es obligatorio."
                        )
                        continue

                    categoria_obj = categorias_cache.get(int(str(categoria_nombre_csv).strip()))
                    # print(categoria_obj)
                    if not categoria_obj:
                        errores_filas.append(
                            f"Línea {line_num} (ID: {materia_id}): Categoría de Materia '{categoria_nombre_csv}' no encontrada en la base de datos. Esta Materia será omitida."
                        )
                        continue

                    # Campos de DimensionesMixin y otros
                    ancho = self._cast_to_decimal(
                        row.get("mp_ancho"), "mp_ancho", line_num, Decimal("0.000")
                    )
                    espesor = self._cast_to_decimal(
                        row.get("mp_espesor_mm"), "mp_espesor_mm", line_num, Decimal("0.000")
                    )
                    peso = self._cast_to_decimal(
                        row.get("mp_peso"), "mp_peso", line_num, Decimal("0.000")
                    )

                    materia_instance = Materia(
                        id=materia_id,
                        nombre=nombre_materia,
                        categoria=categoria_obj,  # Asignar la instancia de CategoriaMateria
                        tipo=row.get("mp_tipo"),
                        composicion=row.get("mp_composicion"),
                        construccion=row.get("mp_construccion"),
                        caracteristica=row.get("mp_caracter"),
                        brillo=row.get("mp_brillo"),
                        grabado=row.get("mp_grabado"),
                        pasadas=self._cast_to_int(
                            row.get("mp_pasadas"), "mp_pasadas", line_num, 0
                        ),
                        # factor=self._cast_to_decimal(
                        #     row.get("factor"), "factor", line_num, Decimal("0.00")
                        # ),
                        costo=self._cast_to_decimal(
                            row.get("mp_costo"), "costo", line_num, Decimal("0.000")
                        ),

                        # Campos de DimensionesMixin
                        ancho=ancho,
                        espesor=espesor,
                        peso=peso,
                        estado=row.get("mp_estado"),
                        obs=row.get("mp_obs"),
                    )
                    materias_a_crear.append(materia_instance)

        except Exception as e:
            raise CommandError(f"Error leyendo CSV para Materia: {e}")

        if errores_filas:
            self.stderr.write(
                self.style.WARNING(
                    f"Se encontraron {len(errores_filas)} errores en filas del CSV de Materias:"
                )
            )
            for error in errores_filas[:10]:
                self.stderr.write(f"- {error}")
            if len(errores_filas) > 10:
                self.stderr.write(f"- ... y {len(errores_filas) - 10} más.")

        if not materias_a_crear:
            self.stdout.write(self.style.WARNING("No hay materias válidas para crear."))
            return

        self.stdout.write(
            f"Preparando para crear {len(materias_a_crear)} materias en lotes de {batch_size}..."
        )
        try:
            with transaction.atomic():
                created_objects = Materia.objects.bulk_create(
                    materias_a_crear,
                    batch_size=batch_size,
                    ignore_conflicts=ignore_conflicts,  # Basado en el 'id' de Materia (PK)
                )

            num_creados = len(created_objects)
            self.stdout.write(
                self.style.SUCCESS(
                    f"¡Importación BULK de Materias completada! Se crearon {num_creados} materias."
                )
            )
            if ignore_conflicts and num_creados < len(materias_a_crear):
                self.stdout.write(
                    self.style.WARNING(
                        f"Se intentaron procesar {len(materias_a_crear)} materias, pero solo {num_creados} fueron creadas (las demás probablemente ya existían y fueron ignoradas)."
                    )
                )

        except Exception as e:
            self.stderr.write(
                self.style.ERROR(f"Error durante bulk_create para Materia: {e}")
            )
            raise CommandError(
                f"Fallo en la operación de bulk_create para Materia: {e}"
            )
