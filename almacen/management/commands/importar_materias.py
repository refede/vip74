import os
import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

# Importamos el Resource
from almacen.resources import MateriaResource
from tablib import Dataset


class Command(BaseCommand):
    help = "Importa Materias y sus características/especificaciones desde un archivo."

    def add_arguments(self, parser):
        parser.add_argument(
            "file_path", type=str, help="La ruta al archivo (CSV o Excel) a importar."
        )
        parser.add_argument(
            "--chunksize",
            type=int,
            default=500,
            help="El número de filas a procesar por lote.",
        )

    def handle(self, *args, **options):
        file_path = options["file_path"]
        chunk_size = options["chunksize"]

        if not os.path.exists(file_path):
            raise CommandError(f"El archivo '{file_path}' no fue encontrado.")

        self.stdout.write(
            self.style.SUCCESS(
                f"Iniciando importación de Materias desde '{file_path}'..."
            )
        )

        materia_resource = MateriaResource()
        total_rows_processed = 0

        # --- INICIO DEL CAMBIO ---

        if file_path.endswith(".csv"):
            # La lógica para CSV con chunksize es correcta y se mantiene
            reader = pd.read_csv(
                file_path, chunksize=chunk_size, keep_default_na=False, dtype=str
            )
            self.process_reader(reader, materia_resource)

        elif file_path.endswith(".xlsx"):
            # 1. Cargar el archivo Excel completo en un DataFrame
            try:
                df = pd.read_excel(file_path, keep_default_na=False, dtype=str)
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Archivo Excel leído correctamente, {len(df)} filas encontradas."
                    )
                )
            except Exception as e:
                raise CommandError(f"Error al leer el archivo Excel: {e}")

            # 2. Procesar el DataFrame en lotes
            self.process_dataframe_in_chunks(df, chunk_size, materia_resource)

        else:
            raise CommandError("Formato de archivo no soportado. Use CSV o XLSX.")

        # --- FIN DEL CAMBIO ---

        self.stdout.write(self.style.SUCCESS(f"\nProceso finalizado."))

    def process_dataframe_in_chunks(self, df, chunk_size, resource):
        """
        Función auxiliar para procesar un DataFrame de pandas en lotes.
        """
        for i in range(0, len(df), chunk_size):
            # Obtenemos el lote (chunk) del DataFrame
            chunk = df.iloc[i : i + chunk_size]
            lote_num = (i // chunk_size) + 1
            self.stdout.write(f"Procesando lote de materias #{lote_num}...")

            # La lógica para convertir el chunk a Dataset y procesarlo es la misma
            self.process_chunk(chunk, resource, lote_num)

    def process_reader(self, reader, resource):
        """
        Función auxiliar para procesar un reader de CSV (que ya viene en lotes).
        """
        for i, chunk in enumerate(reader):
            lote_num = i + 1
            self.stdout.write(f"Procesando lote de materias #{lote_num}...")
            self.process_chunk(chunk, resource, lote_num)

    def process_chunk(self, chunk, resource, lote_num):
        """
        Lógica de importación para un único lote (chunk).
        """
        dataset = Dataset()
        dataset.headers = chunk.columns.tolist()
        for index, row in chunk.iterrows():
            dataset.append(row.tolist())

        try:
            with transaction.atomic():
                result = resource.import_data(
                    dataset, dry_run=False, raise_errors=True, use_transactions=False
                )
        except Exception as e:
            self.stderr.write(
                self.style.ERROR(
                    f"Error en el lote #{lote_num}. Este lote ha sido revertido. Error: {e}"
                )
            )
            return  # Usamos return en lugar de continue

        if not result.has_errors():
            self.stdout.write(
                self.style.SUCCESS(f"  Lote #{lote_num} procesado correctamente.")
            )
