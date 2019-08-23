from django.urls import path

from webapp.views import ClienteRegistro, TarjetaCrear, TarjetaAjaxListView, TarjetaActualizar, ComprasAjaxListView
from . import views
from webapp.views import DireccionCrear, DireccionAjaxListView, DireccionActualizar

app_name = 'webapp'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.index, name='home'),
    path('sitio_en_construccion/', views.sitio_construccion, name='sitio_en_construccion'),
    path('registrar/', ClienteRegistro.as_view(), name='add_cliente'),

    path('editar_perfil/', views.vista_editar_perfil, name='vista_editar_perfil'),
    path('perfil/', views.vista_perfil, name='vista_perfil'),
    path('compras/', ComprasAjaxListView.as_view(), name='tab_list_compras'),
    path('detalle_orden/<int:orden>', views.detalle_orden, name='detalle_orden'),
    path('exclusivas/', views.vista_exclusivas, name='vista_exclusivas'),
    path('marco/<int:producto>', views.vista_marco, name='vista_marco'),
    path('carrito/', views.vista_carrito, name='vista_carrito'),
    path('fotopartners/', views.vista_fotopartners, name='vista_fotopartners'),
    path('foto/<int:pk>', views.vista_foto, name='vista_foto'),
    path('producto_descarga/<token>/<image_name>', views.producto_descarga, name='producto_descarga'),

    #Direccion
    path('direccion/nuevo/', DireccionCrear.as_view(), name='nuevo_direccion'),
    path('direccion/listar/', views.direccion_listar, name='list_direccion'),
    path('direccion/', DireccionAjaxListView.as_view(), name='tab_list_direccion'),
    path('direccion/editar/<int:pk>', DireccionActualizar.as_view(), name='edit_direccion'),
    path('direccion/cambiar_estatus/<int:pk>', views.direccion_cambiar_estatus,
         name='tamanio_cambiar_estatus'),

    # Tarjeta
    path('tarjeta/nuevo/', TarjetaCrear.as_view(), name='nuevo_tarjeta'),
    path('tarjeta/listar/', views.tarjeta_listar, name='list_tarjeta'),
    path('tarjeta/', TarjetaAjaxListView.as_view(), name='tab_list_tarjeta'),
    path('tarjeta/editar/<int:pk>', TarjetaActualizar.as_view(), name='edit_tarjeta'),
    path('tarjeta/cambiar_estatus/<int:pk>', views.tarjeta_cambiar_estatus, name='cambiar_estatus_tarjeta'),
    path('tarjeta/eliminar/<int:pk>', views.tarjeta_eliminar, name='eliminar_tarjeta'),

]