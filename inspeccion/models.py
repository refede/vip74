from django.db import models

from core.choices import *
from core.models import BaseModel
from user.models import Persona


class Unidad(BaseModel):
    id      = models.BigAutoField(primary_key=True)
    simbolo = models.CharField(max_length=30, verbose_name="Símbolo", blank=True, default="", unique=True, db_index=True)

    class Meta:
        ordering = ("simbolo",)
        verbose_name = "Unidad"  # Singular
        verbose_name_plural = "Unidades"  # Plural

    def __str__(self):
        return self.simbolo  # Más simple


class Propiedad(BaseModel):
    id          = models.BigAutoField(primary_key=True)
    nombre      = models.CharField(max_length=50, verbose_name="Nombre", db_index=True)
    unidades    = models.ManyToManyField(Unidad, verbose_name="Unidades", related_name="propiedades", blank=True)
    categoria   = models.CharField(max_length=50, verbose_name="Categoría", blank=True, default="", choices=PROPIEDAD_CHOICES, db_index=True)

    class Meta:
        ordering = ("nombre",)
        verbose_name = "Propiedad"
        verbose_name_plural = "Propiedades"

    def __str__(self):
        return self.nombre  # Más simple


class Equipo(BaseModel):
    id      = models.BigAutoField(primary_key=True)
    nombre  = models.CharField(max_length=50, verbose_name="Nombre", db_index=True)
    marca   = models.CharField(max_length=50, verbose_name="Marca", blank=True, default="")
    modelo  = models.CharField(max_length=50, verbose_name="Modelo", blank=True, default="")
    funcion = models.TextField(verbose_name="Función", blank=True, default="")
    ingreso = models.DateField(verbose_name="Inicio de Servicio", null=True, blank=True)  # null=True es OK para DateField

    class Meta:
        ordering = ("nombre",)
        # Considera unique_together si nombre+marca+modelo deben ser únicos
        # unique_together = [['nombre', 'marca', 'modelo']]
        verbose_name = "Equipo"
        verbose_name_plural = "Equipos"

    def __str__(self):
        parts = [self.nombre, self.marca, self.modelo]
        return " - ".join(filter(None, parts))  # Une partes no vacías


class Metodo(BaseModel):
    id          = models.CharField(primary_key=True, max_length=11, verbose_name="Código")
    nombre      = models.CharField(max_length=100, verbose_name="Nombre", db_index=True)  # Indexar si buscas
    propiedad   = models.ForeignKey(Propiedad, on_delete=models.CASCADE, verbose_name="Propiedad", related_name="metodos", db_index=True)
    norma       = models.CharField(max_length=50, verbose_name="Norma", blank=True, default="")
    muestra     = models.CharField(max_length=500, verbose_name="Muestra", blank=True, default="")
    posicion    = models.DecimalField(decimal_places=2, max_digits=4, verbose_name="Posición", null=True, blank=True)
    velocidad   = models.IntegerField(verbose_name="Velocidad", null=True, blank=True)
    # on_delete=models.PROTECT, # Más seguro que CASCADE

    class Meta:
        ordering = ("id",)
        verbose_name = "Método"
        verbose_name_plural = "Métodos"

    def __str__(self):
        return f"{self.id}-{self.nombre}"


class Instructivo(BaseModel):
    id          = models.CharField(primary_key=True, max_length=11, verbose_name="Código")  # Tu original
    nombre      = models.CharField(max_length=100, verbose_name="Nombre", db_index=True)
    version     = models.IntegerField(verbose_name="Versión", default=1)
    objetivo    = models.TextField(verbose_name="Objetivo", blank=True, default="")
    registro    = models.CharField(max_length=100, verbose_name="Registro", blank=True, default="")
    equipos     = models.ManyToManyField(Equipo, verbose_name="Equipos", related_name="instructivos", blank=True)
    elabora     = models.ForeignKey(Persona, on_delete=models.SET_NULL, verbose_name="Elabora", related_name="instructivos_elaborados", null=True, blank=True, db_index=True)
    revisa      = models.ForeignKey(Persona, on_delete=models.SET_NULL, verbose_name="Revisa", related_name="instructivos_revisados", null=True, blank=True, db_index=True)
    aprueba     = models.ForeignKey(Persona, on_delete=models.SET_NULL, verbose_name="Aprueba", related_name="instructivos_aprobados", null=True, blank=True, db_index=True)
    aprobacion  = models.DateField(verbose_name="Fecha de Aprobación", null=True, blank=True)

    class Meta:
        ordering = ("id",)
        verbose_name = "Instructivo"
        verbose_name_plural = "Instructivos"

    def __str__(self):
        return f"{self.id} - {self.nombre}"


class InstructivoMetodo(BaseModel):
    id          = models.BigAutoField(primary_key=True)
    instructivo = models.ForeignKey(Instructivo, on_delete=models.CASCADE, verbose_name="Instructivo", related_name="metodos_asociados", db_index=True)
    orden       = models.SmallIntegerField(verbose_name="Orden", default=1, db_index=True)
    metodo      = models.ForeignKey(Metodo, on_delete=models.CASCADE, verbose_name="Método", related_name="instructivos_asociados", db_index=True)
    critico     = models.BooleanField(verbose_name="Crítico", default=False)
    requerido   = models.BooleanField(verbose_name="Cuando Aplique", default=False)

    class Meta:
        ordering = ("instructivo","orden",)
        constraints = [
            models.UniqueConstraint(
                fields=["instructivo", "metodo"],
                name="inst_met_unicas",
            )
        ]
        verbose_name = "Método de Instructivo"
        verbose_name_plural = "Métodos de Instructivos"

    def __str__(self):
        inst_str = str(self.instructivo) if self.instructivo else "N/A"
        met_str = str(self.metodo) if self.metodo else "N/A"
        return f"{inst_str} - {met_str}"


class MetodoContenido(BaseModel):
    id          = models.BigAutoField(primary_key=True)
    metodo      = models.ForeignKey(Metodo, on_delete=models.CASCADE, verbose_name="Método", related_name="contenidos", db_index=True)
    tipo        = models.CharField(max_length=50, verbose_name="Tipo", choices=CONTENIDO_CHOICES, db_index=True)
    orden       = models.SmallIntegerField(verbose_name="Orden", db_index=True)
    descripcion = models.TextField(verbose_name="Descripción", blank=True, default="")

    class Meta:
        ordering = (
            "metodo",
            "tipo",
            "orden",
        )  # Ordenar por método primero
        verbose_name = "Contenido de Método"
        verbose_name_plural = "Contenidos de Métodos"

    def __str__(self):
        met_str = str(self.metodo) if self.metodo else "N/A"
        return f"{met_str} - {self.tipo} ({self.orden})"


# class Propiedad(models.Model):
#     """
#     Catálogo central de todas las propiedades medibles.
#     Define QUÉ se puede medir, no cuánto vale.
#     """

#     class TipoDato(models.TextChoices):
#         NUMERO_DECIMAL = "DEC", "Número Decimal"
#         NUMERO_ENTERO = "INT", "Número Entero"

#     nombre = models.CharField(
#         max_length=100,
#         unique=True,
#         help_text="Nombre de la propiedad (ej: Ancho, Espesor).",
#     )
#     descripcion = models.TextField(
#         blank=True, help_text="Explicación de qué es esta propiedad."
#     )
#     tipo_dato = models.CharField(
#         max_length=3, choices=TipoDato.choices, default=TipoDato.NUMERO_DECIMAL
#     )
#     unidad_medida = models.CharField(
#         max_length=20, blank=True, help_text="Unidad de medida (ej: m, g/m, mm)."
#     )

#     class Meta:
#         verbose_name = "Propiedad"
#         verbose_name_plural = "Propiedades"
#         ordering = ["nombre"]

#     def __str__(self):
#         if self.unidad_medida:
#             return f"{self.nombre} ({self.unidad_medida})"
#         return self.nombre
