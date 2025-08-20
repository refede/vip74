from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin

from user.models import User, Persona, Empresa


# Register your models here.
admin.site.register(User)
admin.site.register(Empresa)

class PersonaResource(resources.ModelResource):
    class Meta:
        model = Persona
        import_id_fields = ("id",)

@admin.register(Persona)
class PersonaAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["id", "nombre", "paterno"]
    search_fields = (
        "nombre",
        "paterno",
        "materno",
    )
    ordering = ("id",)
