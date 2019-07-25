from django.urls import path

from webservices.Catalogos import ListCategorias, ListEtiquetas
from webservices.Fotos import SubirFotografia, ListFotosHome, ListMisFotos
from webservices.carrito import AgregarCarrrito, ListCarrito, DeleteCarrito
from webservices.pago import ListDirecciones, ListTarjetas
from webservices.views import ListContactanos

app_name = 'webservices'



urlpatterns = [
    path('list_contactanos/', ListContactanos.as_view(), name='list_contactanos'),
    path('list_categorias/', ListCategorias.as_view(), name='list_categorias'),
    path('list_etiquetas/', ListEtiquetas.as_view(), name='list_etiquetas'),

    path('list_fotos_home/', ListFotosHome.as_view(), name='list_fotos_home'),
    path('list_mis_fotos/', ListMisFotos.as_view(), name='list_mis_fotos'),
    path('subir_foto/', SubirFotografia.as_view(), name='subir_foto'),

    # Carrito
    path('agregar_carrito/', AgregarCarrrito.as_view(), name='agregar_carrito'),
    path('listar_carrito/', ListCarrito.as_view(), name='listar_carrito'),
    path('eliminar_producto_carrito/', DeleteCarrito.as_view(), name='eliminar_producto_carrito'),

    # Pagos
    path('list_direcciones/', ListDirecciones.as_view(), name='list_direcciones'),
    path('list_tarjetas/', ListTarjetas.as_view(), name='list_tarjetas'),

]
