# my_app/management/commands/import_propiedad_unidades_relation.py
import csv
import os
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.conf import settings
from inspeccion.models import Propiedad, Unidad # CAMBIA 'tu_app'

# --- DEFINE LA RUTA A TU CSV AQUÍ ---
CSV_RELATION_PATH = "D:/Users/rflores/Documents/@Refede/Code/db/csv/inspeccion_propiedad_unidades.csv"
#-----------------------------------------

class Command(BaseCommand):
    help = 'Importa relaciones ManyToMany entre Propiedad y Unidad desde un CSV.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--batch-size', type=int, default=1000, # Puede ser mayor para la tabla 'through'
            help='Número de relaciones a crear en cada consulta bulk.'
        )
        # ignore_conflicts es True por defecto para la tabla 'through' en la implementación
        # para evitar errores si la misma relación está duplicada en el CSV.

    def handle(self, *args, **options):
        csv_file_path = CSV_RELATION_PATH
        batch_size = options['batch_size']

        if not os.path.exists(csv_file_path):
            raise CommandError(f"Archivo CSV no encontrado: {csv_file_path}")

        self.stdout.write(self.style.SUCCESS(f"Iniciando importación de relaciones Propiedad-Unidad desde: {csv_file_path}"))

        # Si tu CSV tiene nombres/símbolos en lugar de IDs, necesitarías cargar cachés aquí:
        # propiedades_cache = {p.nombre: p.id for p in Propiedad.objects.all()}
        # unidades_cache = {u.simbolo: u.id for u in Unidad.objects.all()}
        # Y luego, en el bucle, buscar los IDs.
        # Como asumimos que el CSV tiene 'propiedad_id' y 'unidad_id', no se necesitan cachés aquí.

        m2m_relations_to_create = []
        errores_filas = []
        PropiedadUnidadThrough = Propiedad.unidades.through # El modelo de la tabla intermedia

        try:
            with open(csv_file_path, mode='r', encoding='utf-8-sig') as csvfile:
                reader = csv.DictReader(csvfile)
                for i, row in enumerate(reader):
                    line_num = i + 2
                    
                    propiedad_id_str = row.get('propiedad_id')
                    unidad_id_str = row.get('unidad_id')

                    if not propiedad_id_str or not unidad_id_str:
                        errores_filas.append(f"Línea {line_num}: 'propiedad_id' y 'unidad_id' son obligatorios.")
                        continue
                    
                    try:
                        prop_id = int(propiedad_id_str.strip())
                        un_id = int(unidad_id_str.strip())
                    except ValueError:
                        errores_filas.append(f"Línea {line_num}: IDs ('{propiedad_id_str}', '{unidad_id_str}') deben ser números enteros.")
                        continue
                    
                    # Aquí podrías añadir una verificación opcional para ver si los IDs existen
                    # en Propiedad y Unidad si quieres ser extra cuidadoso, pero `ForeignKey`
                    # constraints en la BD deberían manejarlo si los IDs son inválidos (causando error en bulk_create).
                    # if not Propiedad.objects.filter(pk=prop_id).exists():
                    #     errores_filas.append(f"Línea {line_num}: Propiedad ID {prop_id} no existe.")
                    #     continue
                    # if not Unidad.objects.filter(pk=un_id).exists():
                    #     errores_filas.append(f"Línea {line_num}: Unidad ID {un_id} no existe.")
                    #     continue

                    m2m_relations_to_create.append(
                        PropiedadUnidadThrough(
                            propiedad_id=prop_id,
                            unidad_id=un_id
                        )
                    )
        except Exception as e:
            raise CommandError(f"Error leyendo CSV de relaciones Propiedad-Unidad: {e}")

        if errores_filas: # Similar manejo de errores
            self.stderr.write(self.style.WARNING(f"Errores en filas del CSV de relaciones:"))
            for error in errores_filas[:5]: self.stderr.write(f"- {error}")

        if not m2m_relations_to_create:
            self.stdout.write(self.style.WARNING("No hay relaciones Propiedad-Unidad válidas para crear."))
            return

        self.stdout.write(f"Preparando para crear {len(m2m_relations_to_create)} relaciones Propiedad-Unidad...")
        try:
            with transaction.atomic():
                # La PK de la tabla 'through' es (propiedad_id, unidad_id).
                # Usar ignore_conflicts=True es útil para evitar errores si el CSV
                # accidentalmente tiene la misma relación listada múltiples veces.
                PropiedadUnidadThrough.objects.bulk_create(
                    m2m_relations_to_create,
                    batch_size=batch_size,
                    ignore_conflicts=True 
                )
            self.stdout.write(self.style.SUCCESS("¡Importación de relaciones Propiedad-Unidad completada!"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error durante bulk_create para relaciones Propiedad-Unidad: {e}"))
            # Esto podría suceder si un propiedad_id o unidad_id no existe en las tablas principales
            # y no hay 'ON DELETE CASCADE' o similar (o si las FK constraints se verifican).
            raise CommandError(f"Fallo en la operación de bulk_create para relaciones: {e}")