from crum import get_current_user

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from core.choices import *


class BaseModel(models.Model):
    user_creation   = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='%(app_label)s_%(class)s_creation')
    user_updated    = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='%(app_label)s_%(class)s_updated')
    date_creation   = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    date_updated    = models.DateTimeField(auto_now=True, null=True, blank=True)
    estado          = models.BooleanField(verbose_name="Estado", default=True)
    obs             = models.TextField(verbose_name="Observación", null=True, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        user = get_current_user()

        if user and user.is_authenticated: # Asegúrate que el usuario es válido
            if not self.pk:  # El objeto es nuevo si no tiene primary key
                self.user_creation = user
            self.user_updated = user # Siempre actualiza quién modificó

        super().save(*args, **kwargs)


# class DimensionesMixin(models.Model):
    # espesor = models.DecimalField(decimal_places=3, max_digits=8, verbose_name="Espesor", default=0)
    # ancho   = models.DecimalField(decimal_places=3, max_digits=8, verbose_name="Ancho", default=0)
    # peso    = models.DecimalField(decimal_places=3, max_digits=8, verbose_name="Peso", default=0)

    # class Meta:
    #     abstract = True
    # @property
    # def gramaje(self):
    #     if self.ancho and self.ancho != 0: # Asegurarse que ancho no sea None ni cero
    #         return (self.peso / self.ancho) 
    #     return None # O podrías devolver 0 o lanzar una excepción, según tu lógica de negocio

    # def clean(self):
    #     super().clean() # Importante si el modelo que usa el mixin tiene padres
    #     if self.ancho is not None and self.ancho <= 0:
    #         raise ValidationError({'ancho': ('El ancho debe ser un valor positivo.')})
    #     if self.peso is not None and self.peso <= 0:
    #         raise ValidationError({'peso': ('El peso debe ser un valor positivo.')})


class Caracteristica(BaseModel):
    """
    Catálogo central de todas las características.
    """

    nombre = models.CharField(
        max_length=50,
        unique=True,
        help_text="Nombre de la característica.",
    )
    descripcion = models.TextField(
        blank=True, help_text="Explicación de qué es esta característica."
    )
    tipo_dato = models.CharField(
        max_length=3, choices=TIPO_DATO, default="TXT"
    )

    class Meta:
        verbose_name = "Característica"
        verbose_name_plural = "Características"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


