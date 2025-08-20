from django.db import models
from django.contrib.auth.models import AbstractUser

from config.settings import MEDIA_URL, STATIC_URL

from core.choices import *
from core.models import BaseModel


class User(AbstractUser):
    image = models.ImageField(upload_to="users/%Y/%m/%d", null=True, blank=True)

    def get_image(self):
        if self.image:
            return "{}{}".format(MEDIA_URL, self.image)
        return "{}{}{}".format("/", STATIC_URL, "img/empty.png")


class Persona(BaseModel):
    id          = models.BigAutoField(primary_key=True)
    prefijo     = models.CharField(max_length=5, verbose_name="Prefijo", choices=PER_PREFIJO, default="Sr.")
    nombre      = models.CharField(max_length=30, verbose_name="Nombres")
    paterno     = models.CharField(max_length=30, verbose_name="Apellido Paterno")
    materno     = models.CharField(max_length=30, verbose_name="Apellido Materno", blank=True, null=True)
    nickname    = models.CharField(max_length=30, verbose_name="nickname", blank=True, null=True)
    dni         = models.CharField(max_length=8, verbose_name="DNI", blank=True, null=True)
    nacimiento  = models.DateField(verbose_name="Fecha de Nacimiento", blank=True, null=True)
    formacion   = models.CharField(max_length=30, verbose_name="Formación", choices=PER_FORMACION, blank=True, null=True)
    email       = models.EmailField(max_length=30, verbose_name="Email", blank=True, null=True)
    telefono    = models.CharField(max_length=9, verbose_name="Teléfono", blank=True, null=True)
    ingreso     = models.DateField(verbose_name="Fecha de Ingreso", blank=True, null=True)
    departamento= models.CharField(max_length=30, verbose_name="Departamento", choices=PER_DEPARTAMENTO, blank=True, null=True)
    area        = models.CharField(max_length=30, verbose_name="Área", choices=PER_AREA, blank=True, null=True)
    puesto      = models.CharField(max_length=50, verbose_name="Puesto", choices=PER_PUESTO, blank=True, null=True)
    tipo        = models.CharField(max_length=30, verbose_name="Tipo de puesto", choices=PER_TIPO, blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["nombre", "paterno", "dni"],
                name="personas_unicas",
            )
        ]

    def __str__(self):
        return f"{self.nombre} - {self.paterno}"

    def save(self, *args, **kwargs):
        self.nombre  = self.nombre.upper()
        self.paterno = self.paterno.upper()
        self.materno = self.materno.upper()
        super().save()


class Empresa(BaseModel):
    nombre          = models.CharField(max_length=100, unique=True)
    ruc             = models.CharField(max_length=20, unique=True, verbose_name="RUC o NIT")
    direccion       = models.TextField(blank=True, null=True)
    telefono        = models.CharField(max_length=20, blank=True, null=True)
    email           = models.EmailField(blank=True, null=True)
    sitio_web       = models.URLField(blank=True, null=True)
    fecha_creacion  = models.DateField(blank=True, null=True)
    
    def __str__(self):
        return self.nombre
