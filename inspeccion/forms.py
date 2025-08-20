from django import forms
from django.contrib.auth import models
from django.db.models import Q
from django.forms import fields, widgets

from .models import *
from core.forms import BootstrapFormMixin


class EquipoForm(BootstrapFormMixin, forms.ModelForm):
    autofocus_field = "nombre"  # Especifica qué campo debe tener autofocus

    class Meta:
        model = Equipo
        fields = [
            "id",
            "nombre",
            "marca",
            "modelo",
            "funcion",
            "ingreso",
            "estado",
            "obs",
        ]
        widgets = {
            "obs": forms.Textarea(attrs={"rows": 2}),
            "funcion": forms.Textarea(attrs={"rows": 2}),
            "ingreso": forms.DateInput(
                format=("%Y-%m-%d"),
                attrs={"placeholder": "Seleccionar fecha", "type": "date"},
            ),
        }


class UnidadForm(BootstrapFormMixin, forms.ModelForm):
    autofocus_field = "simbolo"  # Especifica qué campo debe tener autofocus

    class Meta:
        model = Unidad
        fields = [
            "simbolo",
            "estado",
            "obs",
        ]
        widgets = {
            "obs": forms.Textarea(attrs={"rows": 2}),
        }


class PropiedadForm(BootstrapFormMixin, forms.ModelForm):
    autofocus_field = "nombre"  # Especifica qué campo debe tener autofocus

    class Meta:
        model = Propiedad
        fields = [
            "nombre",
            "unidades",
            "categoria",
            "estado",
            "obs",
        ]
        widgets = {
            "obs": forms.Textarea(attrs={"rows": 2}),
            "unidades": forms.SelectMultiple(attrs={"size": 7}),
        }


class MetodoForm(BootstrapFormMixin, forms.ModelForm):
    autofocus_field = "id"  # Especifica qué campo debe tener autofocus

    class Meta:
        model = Metodo
        fields = [
            "id",
            "nombre",
            "propiedad",
            "norma",
            "muestra",
            "posicion",
            "velocidad",
            "estado",
            "obs",
        ]
        widgets = {
            "obs": forms.Textarea(attrs={"rows": 2}),
        }


class InstructivoForm(BootstrapFormMixin, forms.ModelForm):
    autofocus_field = "id"  # Especifica qué campo debe tener autofocus

    class Meta:
        model = Instructivo
        fields = [
            "id",
            "nombre",
            "version",
            "objetivo",
            "registro",
            "equipos",
            "elabora",
            "revisa",
            "aprueba",
            "aprobacion",
            "estado",
            "obs",
        ]
        widgets = {
            "objetivo": forms.Textarea(attrs={"rows": 2}),
            "obs": forms.Textarea(attrs={"rows": 2}),
            "aprobacion": forms.DateInput(
                format=("%Y-%m-%d"),
                attrs={"placeholder": "Seleccionar fecha", "type": "date"},
            ),
        }


class InstructivoMetodoForm(BootstrapFormMixin, forms.ModelForm):
    autofocus_field = "orden"  # Especifica qué campo debe tener autofocus

    class Meta:
        model = InstructivoMetodo
        fields = [
            "id",
            "instructivo",
            "orden",
            "metodo",
            "critico",
            "requerido",
            "estado",
            "obs",
        ]
        widgets = {
            "obs": forms.Textarea(attrs={"rows": 2}),
        }

    def clean(self):
        cleaned_data = super().clean()
        instructivo = cleaned_data.get("instructivo")
        metodo = cleaned_data.get("metodo")
        if instructivo and metodo:
            qs = InstructivoMetodo.objects.filter(
                instructivo=instructivo, metodo=metodo
            )
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                self.add_error(
                    None, "La combinación de Instructivo y Método ya existe."
                )
        return cleaned_data


class MetodoContenidoForm(BootstrapFormMixin, forms.ModelForm):
    autofocus_field = "tipo"  # Especifica qué campo debe tener autofocus

    class Meta:
        model = MetodoContenido
        fields = [
            "id",
            "metodo",
            "tipo",
            "orden",
            "descripcion",
            "estado",
            "obs",
        ]
        widgets = {
            "obs": forms.Textarea(attrs={"rows": 2}),
            "descripcion": forms.Textarea(attrs={"rows": 2}),
        }

    def clean(self):
        cleaned_data = super().clean()
        tipo = cleaned_data.get("tipo")
        if tipo is None:
            self.add_error("tipo", "Este campo es obligatorio.")
        return cleaned_data
