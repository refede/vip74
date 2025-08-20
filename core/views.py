from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


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
