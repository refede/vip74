from django.urls import path
from django.contrib.auth import views as auth_views
from core.views import *

app_name = 'core'
urlpatterns = [
    path('', Home.as_view(), name = 'home'),
    path('login/', 	auth_views.LoginView.as_view(template_name='core/login.html'),  name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='core/login.html'), name='logout'),
    path('check-session/', 	check_session, 	name='check_session'),
]
