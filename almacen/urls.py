from django.urls import path, include
from django.contrib.auth import views as auth_views
from almacen.views import *
from . import views


app_name = "almacen"
urlpatterns = [
    # path("categoria/pagina/",           views.categoria_materia_pagina,     name="categoria_materia_pagina"),
    # path("categoria/lista/",            views.categoria_materia_lista,      name="categoria_materia_lista"),
    # path("categoria/data/",             views.categoria_materia_data,       name="categoria_materia_data"),
    # path("categoria/crear/",            views.categoria_materia_crear,      name="categoria_materia_crear"),
    # path("categoria/editar/<pk>/",      views.categoria_materia_editar,     name="categoria_materia_editar"),
    # path("categoria/eliminar/<pk>/",    views.categoria_materia_eliminar,   name="categoria_materia_eliminar"),

    # path('materia/lista/',              views.materia_lista,            name='materia_lista'),
    # path('materia/data/',               views.materia_data,             name='materia_data'),
    # path('materia/crear/',              views.materia_crear,            name='materia_crear'),
    # path('materia/editar/<pk>/',        views.materia_editar,           name='materia_editar'),
    # path('materia/eliminar/<pk>/',      views.materia_eliminar,         name='materia_eliminar'),
    # path('materia/clonar/<pk>/',        views.materia_clonar,           name='materia_clonar'),
    # path('materia/precio_bloque/',      views.materia_costo_bloque,     name='materia_precio_bloque'),
    # path("materia/desactivar/<pk>/",    views.materia_desactivar,       name="materia_desactivar"),
    # path("materia/importar/",           views.materia_importar,         name="materia_importar"),

    # path("proveedor/lista/",            views.proveedor_lista,      name="proveedor_lista"),
    # path("proveedor/data/",             views.proveedor_data,       name="proveedor_data"),
    # path("proveedor/crear/",            views.proveedor_crear,      name="proveedor_crear"),
    # path("proveedor/editar/<pk>/",      views.proveedor_editar,     name="proveedor_editar"),
    # path("proveedor/eliminar/<pk>/",    views.proveedor_eliminar,   name="proveedor_eliminar"),

]