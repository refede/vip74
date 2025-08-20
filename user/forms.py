from django import forms
from django.contrib.auth import models
from django.forms import fields, widgets

from .models import *
from core.forms import BootstrapFormMixin


class PersonaForm(BootstrapFormMixin, forms.ModelForm):
    autofocus_field = "nombre"  # Especifica qué campo debe tener autofocus

    class Meta:
        model = Persona
        fields = [
            "prefijo",
            "nombre",
            "paterno",
            "materno",
            "nickname",
            "dni",
            "nacimiento",
            "formacion",
            "email",
            "telefono",
            "ingreso",
            "departamento",
            "area",
            "puesto",
            "tipo",
            "estado",
            "obs",
        ]
        widgets = {
            "obs": forms.Textarea(attrs={"rows": 2}),
            "nacimiento": forms.DateInput(
                format=("%Y-%m-%d"),
                attrs={"placeholder": "Seleccionar fecha", "type": "date"},
            ),
            "ingreso": forms.DateInput(
                format=("%Y-%m-%d"),
                attrs={"placeholder": "Seleccionar fecha", "type": "date"},
            ),
        }
