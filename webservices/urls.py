from django.urls import path

from webservices.views import ListContactanos, ListCategorias

app_name = 'webservices'



urlpatterns = [
    path('list_contactanos/', ListContactanos.as_view(), name='list_contactanos'),
    path('list_categorias/', ListCategorias.as_view(), name='list_categorias'),

]
