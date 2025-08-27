import logging # Añade este import al principio del archivo

from django import forms
from django.contrib.auth import models
from django.db.models import Q
from django.forms import fields, widgets
from django.core.exceptions import ValidationError

from .models import *
from inspeccion.models import Propiedad
from core.forms import BootstrapFormMixin


class CaracteristicaForm(BootstrapFormMixin, forms.ModelForm):
    autofocus_field = "nombre"  # Especifica qué campo debe tener autofocus

    class Meta:
        model = Caracteristica
        fields = [
            "id",
            "nombre",
            "tipo_dato",
            "estado",
            "obs",
        ]
        widgets = {
            "obs": forms.Textarea(attrs={"rows": 2}),
        }


class CategoriaMateriaForm(BootstrapFormMixin, forms.ModelForm):
    autofocus_field = "nombre"  # Especifica qué campo debe tener autofocus

    caracteristicas = forms.ModelMultipleChoiceField(
        queryset=Caracteristica.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={"class": "choices-multiple"}),
    )
    especificaciones = forms.ModelMultipleChoiceField(
        queryset=Propiedad.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={"class": "choices-multiple"}),
    )

    class Meta:
        model = CategoriaMateria
        fields = [
            "id",
            "nombre",
            "abreviatura",
            "bloque",
            "caracteristicas",
            "especificaciones",
            "estado",
            "obs",
        ]
        widgets = {
            "obs": forms.Textarea(attrs={"rows": 2}),
        }


class MateriaForm(BootstrapFormMixin, forms.ModelForm):
    autofocus_field = "id"  # Especifica qué campo debe tener autofocus

    class Meta:
        model = Materia
        fields = [
            "id",
            "nombre",
            "categoria",
            # "especificaciones",
            "costo",
            # Campos de BaseModel (que no son de auditoría/auto-gestionados)
            "estado",
            "obs",
        ]
        widgets = {
            "obs": forms.Textarea(attrs={"rows": 2}),
        }
    def clean_nombre(self):
        """
        Validador personalizado para el campo 'nombre'.
        Asegura que el nombre sea único, pero excluye al objeto actual
        de la comprobación durante la edición.
        """
        nombre = self.cleaned_data.get('nombre')
        
        # self.instance es el objeto Materia que se está editando.
        # En la creación, self.instance.pk es None.
        if self.instance and self.instance.pk:
            # Estamos editando. Verificamos si existe OTRO objeto con el mismo nombre.
            if Materia.objects.filter(nombre=nombre).exclude(pk=self.instance.pk).exists():
                raise ValidationError("Ya existe otra materia prima con este nombre.", code='unique')
        else:
            # Estamos creando. Verificamos si existe CUALQUIER objeto con este nombre.
            if Materia.objects.filter(nombre=nombre).exists():
                raise ValidationError("Ya existe una materia prima con este nombre.", code='unique')
                
        return nombre

# class ProveedorForm(BootstrapFormMixin, forms.ModelForm):
#     autofocus_field = "nombre"

#     class Meta:
#         model = Proveedor
#         fields = [
#             "nombre",
#             "abreviatura",
#             "procedencia",
#             "ruc",
#             # Campos de BaseModel (que no son de auditoría/auto-gestionados)
#             "estado",
#             "obs",
#         ]
#         widgets = {
#             "obs": forms.Textarea(attrs={"rows": 2}),
#         }


class MateriaClonarForm(BootstrapFormMixin, forms.Form):
    autofocus_field = "nuevo_id"
    nuevo_id = forms.CharField(label="Nuevo Código", max_length=9, required=True)


class MateriaCostoBloqueForm(BootstrapFormMixin, forms.Form):
    autofocus_field = "categoria_objetivo"
    categoria_objetivo = forms.ModelChoiceField(
        label="Categoría", queryset=CategoriaMateria.objects.filter(Q(bloque=True))
    )
    costo_bloque = forms.DecimalField(
        label="Costo de Bloque", decimal_places=3, max_digits=10, required=True
    )
