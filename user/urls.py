from django.urls import path, include
from django.contrib.auth import views as auth_views
from user.views import *
from . import views


app_name = "user"
urlpatterns = [
    path('persona/lista/',          views.persona_lista,       name='persona_lista'),
    path('persona/data/',           views.persona_data,        name='persona_data'),
    path('persona/crear/',          views.persona_crear,       name='persona_crear'),
    path('persona/editar/<pk>/',    views.persona_editar,      name='persona_editar'),
    path('persona/eliminar/<pk>/',  views.persona_eliminar,    name='persona_eliminar'),
]
