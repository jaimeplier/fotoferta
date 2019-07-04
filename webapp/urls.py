from django.urls import path

from webapp.views import ClienteRegistro
from . import views

app_name = 'webapp'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('sitio_en_construccion/', views.sitio_construccion, name='sitio_en_construccion'),
    path('registrar/', ClienteRegistro.as_view(), name='add_cliente'),
]