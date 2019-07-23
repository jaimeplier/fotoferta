from django.urls import path

from webapp.views import ClienteRegistro
from . import views

app_name = 'webapp'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.index, name='home'),
    path('sitio_en_construccion/', views.sitio_construccion, name='sitio_en_construccion'),
    path('registrar/', ClienteRegistro.as_view(), name='add_cliente'),

    path('editar_perfil/', views.vista_editar_perfil, name='vista_editar_perfil'),
    path('perfil/', views.vista_perfil, name='vista_perfil'),
    path('exclusivas/', views.vista_exclusivas, name='vista_exclusivas'),
    path('marco/', views.vista_marco, name='vista_marco'),
    path('carrito/', views.vista_carrito, name='vista_carrito'),
    path('foto/<int:pk>', views.vista_foto, name='vista_foto'),

]