from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect


urlpatterns = [
    path("admin/",          admin.site.urls),
    # path("favicon.ico",     lambda _ : redirect('static/img/favicon.png', permanent=True)),
    path("",                include("core.urls")),
    path("user/",           include("user.urls")),
    # path("almacen/",        include("almacen.urls")),
    path("inspeccion/",     include("inspeccion.urls")),
    # path("procesamiento/",  include("procesamiento.urls")),
    # path("productos/",      include("productos.urls")),
    # path("ventas/",  		include("ventas.urls")),
    # path("dyd/",           	include("dyd.urls")),
    # path("dashboard/",      include("dashboard.urls")),

    # path("demo/",           include("demo.urls")),
    # path("finanzas/",   include("finanzas.urls")),
    # path("salud/",      include("salud.urls")),  
    # path('chaining/',   include('smart_selects.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        # path('__debug__/', include(debug_toolbar.urls)),
    ]