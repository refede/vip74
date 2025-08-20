# en mi_app/middleware.py
from django.http import HttpResponseForbidden
from django.conf import settings
from django.shortcuts import redirect
from urllib.parse import urlencode

class HtmxLoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Primero, deja pasar la respuesta normal
        response = self.get_response(request)

        # Si la respuesta es una redirección al LOGIN_URL
        # Y la petición original era de HTMX
        # Y el usuario no está autenticado
        if (response.status_code == 302 and
            settings.LOGIN_URL in response.url and
            request.htmx and
            not request.user.is_authenticated):

            # Devuelve 403 Forbidden en lugar de la redirección
            # para que el JS del lado del cliente lo maneje.
            return HttpResponseForbidden("Authentication required.")

        return response

# --- Alternativa: Interceptar antes (más directo pero afecta a todas las 403/401) ---
# class HtmxHandle40xMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         response = self.get_response(request)
#         return response

#     def process_view(self, request, view_func, view_args, view_kwargs):
#         # Ejecuta la vista decorada con @login_required (o similar)
#         # Si la vista requiere login Y el usuario no está logueado
#         if not request.user.is_authenticated:
#             # Verifica si la vista tiene el atributo _login_required
#             # (Esto es un detalle interno, podría cambiar en futuras versiones de Django)
#             # O simplemente verifica si es una petición HTMX
#             if getattr(view_func, 'login_required', False) or request.htmx:
#                  # Verifica explícitamente que no sea la vista de login
#                  login_url_path = settings.LOGIN_URL.split('?')[0]
#                  if request.path != login_url_path:
#                       if request.htmx:
#                            # Para HTMX, devuelve 403 para que lo capture el JS
#                            print("HTMX request requires login, returning 403") # Log
#                            return HttpResponseForbidden("Authentication required.")
#                       else:
#                            # Para no-HTMX, redirige como siempre
#                            login_url = settings.LOGIN_URL
#                            next_url = request.get_full_path()
#                            redirect_url = f"{login_url}?{urlencode({'next': next_url})}"
#                            return redirect(redirect_url)
#         return None # Continúa con la vista normal si está autenticado