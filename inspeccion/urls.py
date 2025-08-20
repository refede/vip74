from django.urls import path, include
from django.contrib.auth import views as auth_views

from inspeccion.views import *
from . import views


app_name = 'inspeccion'
urlpatterns = [
    path('equipo/lista/',          views.equipo_lista,     name='equipo_lista'),
    path('equipo/data/',           views.equipo_data,      name='equipo_data'),
    path('equipo/crear/',          views.equipo_crear,     name='equipo_crear'),
    path('equipo/editar/<pk>/',    views.equipo_editar,    name='equipo_editar'),
    path('equipo/eliminar/<pk>/',  views.equipo_eliminar,  name='equipo_eliminar'),

    path('unidad/lista/',           views.unidad_lista,     name='unidad_lista'),
    path('unidad/data/',            views.unidad_data,      name='unidad_data'),
    path('unidad/crear/',           views.unidad_crear,     name='unidad_crear'),
    path('unidad/editar/<pk>/',     views.unidad_editar,    name='unidad_editar'),
    path('unidad/eliminar/<pk>/',   views.unidad_eliminar,  name='unidad_eliminar'),

    path('propiedad/lista/',            views.propiedad_lista,     name='propiedad_lista'),
    path('propiedad/data/',             views.propiedad_data,      name='propiedad_data'),
    path('propiedad/crear/',            views.propiedad_crear,     name='propiedad_crear'),
    path('propiedad/editar/<pk>/',      views.propiedad_editar,    name='propiedad_editar'),
    path('propiedad/eliminar/<pk>/',    views.propiedad_eliminar,  name='propiedad_eliminar'),

    path('metodo/lista/',                           views.metodo_lista,                     name='metodo_lista'),
    path('metodo/data/',                            views.metodo_data,                      name='metodo_data'),
    path('metodo/crear/',                           views.metodo_crear,                     name='metodo_crear'),
    path('metodo/editar/<pk>/',                     views.metodo_editar,                    name='metodo_editar'),
    path('metodo/editar/parcial/<pk>/',             views.metodo_editar_parcial,            name='metodo_editar_parcial'),
    path('metodo/eliminar/<pk>/',                   views.metodo_eliminar,                  name='metodo_eliminar'),
    path('metodo/detalle/<pk>/',                    views.metodo_detalle,                   name='metodo_detalle'),
    path('metodo/detalle/caracteristicas/<pk>/',    views.metodo_detalle_caracteristicas,   name='metodo_detalle_caracteristicas'),
    path('metodo/detalle/contenido/<pk>/',          views.metodo_detalle_contenido,         name='metodo_detalle_contenido'),

    path('instructivo/lista/',                              views.instructivo_lista,                    name='instructivo_lista'),
    path('instructivo/data/',                               views.instructivo_data,                     name='instructivo_data'),
    path('instructivo/crear/',                              views.instructivo_crear,                    name='instructivo_crear'),
    path('instructivo/editar/<str:pk>/',                    views.instructivo_editar,                   name='instructivo_editar'),
    path('instructivo/editar/parcial/<str:pk>/',            views.instructivo_editar_parcial,           name='instructivo_editar_parcial'),
    path('instructivo/eliminar/<str:pk>/',                  views.instructivo_eliminar,                 name='instructivo_eliminar'),
    path('instructivo/detalle/<str:pk>/',                   views.instructivo_detalle,                  name='instructivo_detalle'),
    path('instructivo/detalle/caracteristicas/<str:pk>/',   views.instructivo_detalle_caracteristicas,  name='instructivo_detalle_caracteristicas'),
    path('instructivo/detalle/contenido/<pk>/',             views.instructivo_detalle_contenido,        name='instructivo_detalle_contenido'),

    path('instructivo_metodo/lista/',                       views.instructivo_metodo_lista,     name='instructivo_metodo_lista'),
    path('instructivo_metodo/data/',                        views.instructivo_metodo_data,      name='instructivo_metodo_data'),
    path('instructivo_metodo/crear/<str:instructivo_id>/',  views.instructivo_metodo_crear,     name='instructivo_metodo_crear'),
    path('instructivo_metodo/editar/<pk>/',                 views.instructivo_metodo_editar,    name='instructivo_metodo_editar'), # new
    path('instructivo_metodo/eliminar/<pk>/',               views.instructivo_metodo_eliminar,  name='instructivo_metodo_eliminar'),

    path('metodo_contenido/lista/',                views.metodo_contenido_lista,     name='metodo_contenido_lista'),
    path('metodo_contenido/data/',                 views.metodo_contenido_data,      name='metodo_contenido_data'),
    path('metodo_contenido/crear/<str:metodo_id>', views.metodo_contenido_crear,     name='metodo_contenido_crear'),
    path('metodo_contenido/editar/<pk>/',          views.metodo_contenido_editar,    name='metodo_contenido_editar'), # new
    path('metodo_contenido/eliminar/<pk>/',        views.metodo_contenido_eliminar,  name='metodo_contenido_eliminar'),

    # path('actividad/<metodo>/crear/',   Actividadcrear.as_view(),       name='actividad_nuevo'),
    # path('actividad/editar/<pk>/',      ActividadEditar.as_view(),      name='actividad_editar'), # new
    # path('actividad/eliminar/<pk>/',    ActividadEliminar.as_view(),    name='actividad_eliminar'),

    # path('calificativo/<metodo>/nuevo/',CalificativoNuevo.as_view(),    name='calificativo_nuevo'),
    # path('calificativo/editar/<pk>/',   CalificativoEditar.as_view(),   name='calificativo_editar'), # new
    # path('calificativo/eliminar/<pk>/', CalificativoEliminar.as_view(), name='calificativo_eliminar'),
    
    # path('soporte/lista/',          EvaluacionSoporteLista.as_view(),   name='evaluacion_soporte_lista'),
    # path('soporte/nuevo/',          EvaluacionSoporteNuevo.as_view(),   name='evaluacion_soporte_nuevo'),
    # path('soporte/editar/<pk>/',    EvaluacionSoporteEditar.as_view(),  name='evaluacion_soporte_editar'), # new
    # path('soporte/eliminar/<pk>/',  EvaluacionSoporteEliminar.as_view(),name='evaluacion_soporte_eliminar'),
    # path('soporte/detalle/<pk>/',   views.evaluacion_soporte_detalle,   name='evaluacion_soporte_detalle'),

    # path('soporte/datos/<pk>/nuevo/',       DatosEvaluacionSoporteNuevo.as_view(),      name='datos_evaluacion_soporte_nuevo'),
    # path('soporte/datos/editar/<pk>/',      DatosEvaluacionSoporteEditar.as_view(),     name='datos_evaluacion_soporte_editar'),
    # path('soporte/datos/eliminar/<pk>/',    DatosEvaluacionSoporteEliminar.as_view(),   name='datos_evaluacion_soporte_eliminar'),

    # path('muestra_mp/lista/',          EvaluacionMuestraMPLista.as_view(),   name='evaluacion_muestra_mp_lista'),
    # path('muestra_mp/nuevo/',          EvaluacionMuestraMPNuevo.as_view(),   name='evaluacion_muestra_mp_nuevo'),
    # path('muestra_mp/editar/<pk>/',    EvaluacionMuestraMPEditar.as_view(),  name='evaluacion_muestra_mp_editar'), # new
    # path('muestra_mp/eliminar/<pk>/',  EvaluacionMuestraMPEliminar.as_view(),name='evaluacion_muestra_mp_eliminar'),
    # path('muestra_mp/detalle/<pk>/',   views.evaluacion_muestra_mp_detalle,  name='evaluacion_muestra_mp_detalle'),
    # path('muestra_mp/clonar/',         ClonarEvaluacionMuestraMP.as_view(),  name='clonar_evaluacion_muestra_mp'),
    
    # path('rea/lista/',           REALista.as_view(),       name='rea_lista'),
    # path('rea/nuevo/',           REANuevo.as_view(),       name='rea_nuevo'),
    # path('rea/editar/<pk>/',     REAEditar.as_view(),      name='rea_editar'),
    # path('rea/detalle/<pk>/',    views.rea_detalle,        name='rea_detalle'),
    # path('rea/valor/nuevo/<int:arg_partida>/<int:arg_propiedad>/', views.rea_valor_nuevo, name='rea_valor_nuevo'),
    # path('rea/valor/editar/<pk>/', ReaValorEditar.as_view(),                              name='rea_valor_editar'),

    # path('rea/articulo/clonar/',          ClonarFicha.as_view(),    name='rea_clonar'),



]