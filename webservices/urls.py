from django.urls import path

from webservices.Catalogos import ListCategorias, ListEtiquetas
from webservices.Fotos import SubirFotografia, ListFotosHome, ListMisFotos, ListFotosRecomendadas
from webservices.Interaccion import ListFavoritos, AgregarFavoritos, ListSiguiendo, SeguirFotopartner, ListFotopartners
from webservices.carrito import AgregarCarrrito, ListCarrito, DeleteCarrito, ModificarProductoCarrito, ListMarco, \
    ListTamanio, ListTipoPapel, ListTexturas, ListMariaLuisa
from webservices.pago import ListDirecciones, ListTarjetas, PagarOrden
from webservices.views import ListContactanos, ListDatosCP, ListRedesSociales, Signin

app_name = 'webservices'



urlpatterns = [
    # Registro redes sociales
    path('registro_redes/', Signin.as_view(), name='registro_redes'),
    path('list_redes_sociales/', ListRedesSociales.as_view(), name='list_redes_sociales'),

    path('list_contactanos/', ListContactanos.as_view(), name='list_contactanos'),
    path('list_categorias/', ListCategorias.as_view(), name='list_categorias'),
    path('list_etiquetas/', ListEtiquetas.as_view(), name='list_etiquetas'),
    path('list_colonias/', ListDatosCP.as_view(), name='list_colonias'),

    path('list_fotos_home/', ListFotosHome.as_view(), name='list_fotos_home'),
    path('list_fotos_recomendadas/', ListFotosRecomendadas.as_view(), name='list_fotos_recomendadas'),
    path('list_mis_fotos/', ListMisFotos.as_view(), name='list_mis_fotos'),
    path('subir_foto/', SubirFotografia.as_view(), name='subir_foto'),

    # Carrito
    path('agregar_carrito/', AgregarCarrrito.as_view(), name='agregar_carrito'),
    path('modificar_producto_carrito/', ModificarProductoCarrito.as_view(), name='modificar_producto_carrito'),
    path('listar_carrito/', ListCarrito.as_view(), name='listar_carrito'),
    path('eliminar_producto_carrito/', DeleteCarrito.as_view(), name='eliminar_producto_carrito'),
    path('listar_marcos/', ListMarco.as_view(), name='listar_marcos'),
    path('listar_marialuisa/', ListMariaLuisa.as_view(), name='listar_marialuisa'),
    path('listar_tamanios/', ListTamanio.as_view(), name='listar_tamanios'),
    path('listar_tipos_papel/', ListTipoPapel.as_view(), name='listar_tipos_papel'),
    path('listar_texturas/', ListTexturas.as_view(), name='listar_listar_texturas'),


    # Pagos
    path('list_direcciones/', ListDirecciones.as_view(), name='list_direcciones'),
    path('list_tarjetas/', ListTarjetas.as_view(), name='list_tarjetas'),
    path('pagar_orden/', PagarOrden.as_view(), name='pagar_orden'),

    # Interacciones
    path('list_favoritos/', ListFavoritos.as_view(), name='list_favoritos'),
    path('favorito/', AgregarFavoritos.as_view(), name='favorito'),
    path('list_siguiendo/', ListSiguiendo.as_view(), name='list_siguiendo'),
    path('seguir/', SeguirFotopartner.as_view(), name='seguir'),
    path('list_fotopartners/', ListFotopartners.as_view(), name='list_fotopartners'),

]
