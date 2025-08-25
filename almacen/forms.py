from django import forms
from django.contrib.auth import models
from django.db.models import Q
from django.forms import fields, widgets

from .models import *
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

    class Meta:
        model = CategoriaMateria
        fields = [
            "id",
            "nombre",
            "abreviatura",
            "bloque",
            "caracteristicas",
            "estado",
            "obs",
        ]
        widgets = {
            "obs": forms.Textarea(attrs={"rows": 2}),
            "caracteristicas": forms.MultipleHiddenInput(),
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
    nuevo_id = forms.CharField(label="Nuevo Código", max_length=9, required=True)
    autofocus_field = "nuevo_id"


class MateriaCostoBloqueForm(BootstrapFormMixin, forms.Form):
    categoria_objetivo = forms.ModelChoiceField(
        label="Categoría", queryset=CategoriaMateria.objects.filter(Q(bloque=True))
    )
    costo_bloque = forms.DecimalField(
        label="Costo de Bloque", decimal_places=3, max_digits=10, required=True
    )
    autofocus_field = "categoria_objetivo"
