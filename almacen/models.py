from django.db import models

from core.models import BaseModel
from core.choices import *


class Caracteristica(BaseModel):
    """
    Catálogo central de todas las características.
    """

    tipo_dato   = models.CharField(max_length=3, choices=TIPO_DATO, default="TXT")
    nombre      = models.CharField(max_length=50, unique=True, help_text="Nombre de la característica.",)

    class Meta:
        verbose_name = "Característica"
        verbose_name_plural = "Características"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class CategoriaMateria(BaseModel):
    id                  = models.BigAutoField(primary_key=True)
    nombre              = models.CharField(max_length=60, unique=True, verbose_name="Nombre")
    abreviatura         = models.CharField(max_length=25, unique=True, verbose_name="Abreviatura")
    bloque              = models.BooleanField(verbose_name="Bloque", default=False)
    caracteristicas     = models.ManyToManyField(Caracteristica, blank=True, verbose_name="Características", related_name="categoria_caracteristicas")
    especificaciones    = models.ManyToManyField('inspeccion.Propiedad', verbose_name="Especificaciones", related_name="categoria_especificaciones")

    class Meta:
        verbose_name = "Categoría de MP"
        verbose_name_plural = "Categorías de MP"
        ordering = ("id",)

    def __str__(self):
        return self.nombre


class Materia(BaseModel):
    id                  = models.CharField(primary_key=True, max_length=9, verbose_name="Código")
    nombre              = models.CharField(max_length=50, unique=True, verbose_name="Nombre")
    categoria           = models.ForeignKey(CategoriaMateria, on_delete=models.CASCADE, verbose_name="Categoría", related_name="categoria_materia")
    costo               = models.DecimalField(decimal_places=3, max_digits=10, verbose_name="Costo", null=True, blank=True)

    class Meta:
        verbose_name = "Materia Prima"
        verbose_name_plural = "Materias Primas"
        ordering = ("id",)

    def __str__(self):
        return f'{self.id} - {self.nombre}'

    # @property
    # def espesor_mil(self):
    #     return round((self.espesor*40), 0)

    # @property
    # def costo_unitario(self):
    #     return round((self.costo*self.peso/1000), 3)

    # @property
    # def costo_papel(self):
    #     return round(((self.costo*self.peso/1000)/self.pasadas), 3)


class CaracteristicaMateria(BaseModel):
    """
    Modelo "Through" mejorado. Ahora une la Materia con una Caracteristica
    y le asigna el valor específico para esa Materia.
    """

    materia         = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name="valores_caracteristicas")
    caracteristica  = models.ForeignKey(Caracteristica, on_delete=models.CASCADE, related_name="valores_en_materias")
    valor           = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        verbose_name = "Característica de MP"
        verbose_name_plural = "Características de MP"
        unique_together = ('materia', 'caracteristica') 

    def __str__(self):
        return f"{self.materia.nombre} - {self.caracteristica.nombre}: {self.valor}"


class EspecificacionMateria(BaseModel):
    """
    Modelo "Through" que une una Materia Prima con una Propiedad y le asigna
    un valor y reglas de evaluación.
    """

    materia     = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name="propiedades_especificas")
    propiedad   = models.ForeignKey('inspeccion.Propiedad', on_delete=models.CASCADE)
    valor       = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)

    # tolerancia_positiva = models.DecimalField(
    #     max_digits=10, decimal_places=3, null=True, blank=True
    # )

    # tolerancia_negativa = models.DecimalField(
    #     max_digits=10, decimal_places=3, null=True, blank=True
    # )

    class Meta:
        verbose_name = "Especificación de MP"
        verbose_name_plural = "Especificaciones de MP"
        unique_together = ("materia", "propiedad")

    def __str__(self):
        return f"{self.materia.nombre} - {self.propiedad.nombre}: {self.valor}"

