# my_app/management/commands/import_categorias_materia.py
import csv
import os
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.conf import settings
# Asegúrate de que la ruta a tus modelos sea correcta
from almacen.models import CategoriaMateria # CAMBIA 'tu_app' por el nombre de tu app

# --- DEFINE LA RUTA A TU CSV AQUÍ ---
CSV_CATEGORIAS_PATH = "D:/Users/rflores/Documents/@Refede/Code/db/csv/materias_categoriamp.csv"
#-----------------------------------------

class Command(BaseCommand):
    help = 'Importa NUEVAS Categorías de Materia desde un CSV (ruta hardcodeada) usando bulk_create.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--batch-size', type=int, default=500,
            help='Número de objetos a crear en cada consulta bulk.'
        )
        parser.add_argument(
            '--ignore-conflicts', action='store_true',
            help='Si se especifica, ignora filas que causarían conflictos de unicidad (nombre, abreviatura).'
        )

    def _parse_boolean(self, value_str):
        """Convierte strings a booleano de forma flexible."""
        value_str_lower = str(value_str).lower().strip()
        if value_str_lower in ('true', 't', '1', 'yes', 'y', 'si', 'sí'):
            return True
        if value_str_lower in ('false', 'f', '0', 'no', 'n'):
            return False
        # Podrías levantar un error o retornar un default si el valor no es reconocido
        self.stderr.write(self.style.WARNING(f"Valor booleano no reconocido '{value_str}', se asume False."))
        return False


    def handle(self, *args, **options):
        csv_file_path = CSV_CATEGORIAS_PATH
        batch_size = options['batch_size']
        ignore_conflicts = options['ignore_conflicts']

        if not os.path.exists(csv_file_path):
            raise CommandError(f"Archivo CSV no encontrado: {csv_file_path}")

        self.stdout.write(self.style.SUCCESS(f"Iniciando importación BULK para CategoriaMateria desde: {csv_file_path}"))

        categorias_a_crear = []
        errores_filas = []

        try:
            with open(csv_file_path, mode='r', encoding='utf-8-sig') as csvfile:
                reader = csv.DictReader(csvfile)
                for i, row in enumerate(reader):
                    line_num = i + 2 # +1 por encabezado, +1 por 0-indexed

                    id = row.get('id')
                    nombre = row.get('cat_nombre')
                    abreviatura = row.get('cat_abreviado')
                    bloque_str = row.get('cat_precio')

                    if not nombre or not abreviatura:
                        errores_filas.append(f"Línea {line_num}: 'nombre' y 'abreviatura' son obligatorios.")
                        continue
                    
                    # Validar unicidad de nombre y abreviatura si no se usa ignore_conflicts
                    # (Este chequeo es más para evitar problemas en la lista Python,
                    # ignore_conflicts lo manejará a nivel BD si está activo)
                    # if not ignore_conflicts:
                    #     if any(c.nombre == nombre for c in categorias_a_crear) or \
                    #        any(c.abreviatura == abreviatura for c in categorias_a_crear):
                    #         errores_filas.append(f"Línea {line_num}: Nombre '{nombre}' o Abreviatura '{abreviatura}' duplicado en el CSV.")
                    #         continue

                    categoria_instance = CategoriaMateria(
                        id=id,
                        nombre=nombre,
                        abreviatura=abreviatura,
                        bloque=self._parse_boolean(bloque_str)
                    )
                    categorias_a_crear.append(categoria_instance)

        except Exception as e:
            raise CommandError(f"Error leyendo CSV para CategoriaMateria: {e}")

        if errores_filas:
            self.stderr.write(self.style.WARNING(f"Se encontraron {len(errores_filas)} errores en filas del CSV de Categorías:"))
            for error in errores_filas[:10]: self.stderr.write(f"- {error}")
            if len(errores_filas) > 10: self.stderr.write(f"- ... y {len(errores_filas) - 10} más.")

        if not categorias_a_crear:
            self.stdout.write(self.style.WARNING("No hay categorías válidas para crear."))
            return

        self.stdout.write(f"Preparando para crear {len(categorias_a_crear)} categorías en lotes de {batch_size}...")
        try:
            with transaction.atomic():
                created_objects = CategoriaMateria.objects.bulk_create(
                    categorias_a_crear,
                    batch_size=batch_size,
                    ignore_conflicts=ignore_conflicts
                )
            
            num_creados = len(created_objects)
            # Con ignore_conflicts=True, Django no establece los PKs en los objetos de la lista si hubo conflictos.
            # created_objects contendrá solo los que se insertaron.
            self.stdout.write(self.style.SUCCESS(f"¡Importación BULK de Categorías completada! Se crearon {num_creados} categorías."))
            if ignore_conflicts and num_creados < len(categorias_a_crear):
                self.stdout.write(self.style.WARNING(
                    f"Se intentaron procesar {len(categorias_a_crear)} categorías, pero solo {num_creados} fueron creadas (las demás probablemente ya existían y fueron ignoradas)."
                ))

        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error durante bulk_create para CategoriaMateria: {e}"))
            raise CommandError(f"Fallo en la operación de bulk_create para CategoriaMateria: {e}")