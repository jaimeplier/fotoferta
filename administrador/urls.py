from django.urls import path

from administrador import views
from administrador.views import CodigoMarcoCrear, CodigoMarcoListarAjaxListView, CodigoMarcoActualizar

app_name = 'administrador'
urlpatterns = [

    path('codigo_marco/nuevo/', CodigoMarcoCrear.as_view(), name='nuevo_codigo_marco'),
    path('codigo_marco/listar/', views.codigo_marco_listar, name='list_codigo_marco'),
    path('tabla_codigo_marco/', CodigoMarcoListarAjaxListView.as_view(), name='tab_list_codigo_marco'),
    path('codigo_marco/editar/<int:pk>', CodigoMarcoActualizar.as_view(), name='edit_codigo_marco'),
]