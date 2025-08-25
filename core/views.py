import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, HttpResponseRedirect, render
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView

# from .models import Caracteristica
# from .forms import CaracteristicaForm

# Create your views here.
class Home(LoginRequiredMixin, TemplateView):
    template_name = "core/home.html"
    # login_url = 'bases:login'


@login_required
def check_session(request):
    if request.user.is_authenticated:
        return JsonResponse({"active": True})
    else:
        return JsonResponse({"active": False})


