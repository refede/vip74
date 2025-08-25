from django import forms
from .models import *


class BootstrapFormMixin:
    """
    Mixin para añadir clases CSS de Bootstrap a los widgets del formulario
    y manejar el atributo autofocus.
    """
    autofocus_field = None # Define esto en la clase que usa el Mixin

    def __init__(self, *args, **kwargs):
        # ¡Importante! Llamar al __init__ de la clase padre (ModelForm) primero
        super().__init__(*args, **kwargs)

        # Aplicar clases CSS
        for field_name, field in self.fields.items():
            widget = field.widget
            # Clases a aplicar
            default_classes = ["form-control", "form-control-sm"]
            checkbox_classes = ["form-check-input"]

            # Obtener clases actuales y evitar duplicados
            current_classes_str = widget.attrs.get("class", "")
            current_classes_set = set(current_classes_str.split())
            classes_to_add = []

            if isinstance(widget, forms.CheckboxInput):
                for cls in checkbox_classes:
                    if cls not in current_classes_set:
                        classes_to_add.append(cls)
            elif not isinstance(
                widget,
                (
                    forms.CheckboxSelectMultiple,
                    forms.RadioSelect,
                    forms.FileInput,
                    forms.ClearableFileInput,
                    # Podrías añadir otros widgets aquí si no deben tener form-control
                ),
            ):
                for cls in default_classes:
                    if cls not in current_classes_set:
                        classes_to_add.append(cls)

            # Añadir las nuevas clases si las hay
            if classes_to_add:
                final_classes = current_classes_str.split() + classes_to_add
                widget.attrs["class"] = " ".join(filter(None, final_classes))

        # Aplicar autofocus si se definió el campo y existe en el form
        if self.autofocus_field and self.autofocus_field in self.fields:
            self.fields[self.autofocus_field].widget.attrs["autofocus"] = True
        # else:
        #     # Opcional: Poner autofocus en el primer campo si no se especifica uno
        #     first_field_name = next(iter(self.fields), None)
        #     if first_field_name:
        #        self.fields[first_field_name].widget.attrs['autofocus'] = True


class ImportarForm(BootstrapFormMixin, forms.Form):
    csv_file = forms.FileField(label="Seleccione un archivo CSV")


class ImportarXmlForm(BootstrapFormMixin, forms.Form):
    xml_file = forms.FileField(label="Seleccione un archivo XML")


