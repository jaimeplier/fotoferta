from django.urls import path

from webservices.Catalogos import ListCategorias, ListEtiquetas
from webservices.Fotos import SubirFotografia, ListFotosHome
from webservices.views import ListContactanos

app_name = 'webservices'



urlpatterns = [
    path('list_contactanos/', ListContactanos.as_view(), name='list_contactanos'),
    path('list_categorias/', ListCategorias.as_view(), name='list_categorias'),
    path('list_etiquetas/', ListEtiquetas.as_view(), name='list_etiquetas'),

    path('list_fotos_home/', ListFotosHome.as_view(), name='list_fotos_home'),
    path('subir_foto/', SubirFotografia.as_view(), name='subir_foto'),

]
