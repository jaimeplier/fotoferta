from django.urls import path

from webapp.views import ClienteRegistro
from . import views
from webapp.views import DireccionCrear, DireccionListarAjaxListView, DireccionActualizar

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

    #Direccion
    path('direccion/nuevo/', DireccionCrear.as_view(), name='nuevo_direccion'),
    path('direccion/listar/', views.direccion_listar, name='list_direccion'),
    path('direccion/', DireccionListarAjaxListView.as_view(), name='tab_list_direccion'),
    path('direccion/editar/<int:pk>', DireccionActualizar.as_view(), name='edit_direccion'),
    path('direccion/cambiar_estatus/<int:pk>', views.direccion_cambiar_estatus,
         name='tamanio_cambiar_estatus'),

]