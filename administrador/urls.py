from django.urls import path

from administrador import views
from administrador.views import CodigoMarcoCrear, CodigoMarcoListarAjaxListView, CodigoMarcoActualizar, TamanioCrear, \
    TamanioListarAjaxListView, TamanioActualizar, MarcoCrear, MarcoListarAjaxListView, MarcoActualizar, MarialuisaCrear, \
    MarialuisaAjaxListView, MarialuisaActualizar, ModeloMarialuisaCrear, ModeloMarialuisaAjaxListView, ModeloMarialuisaActualizar

app_name = 'administrador'
urlpatterns = [

    path('codigo_marco/nuevo/', CodigoMarcoCrear.as_view(), name='nuevo_codigo_marco'),
    path('codigo_marco/listar/', views.codigo_marco_listar, name='list_codigo_marco'),
    path('tabla_codigo_marco/', CodigoMarcoListarAjaxListView.as_view(), name='tab_list_codigo_marco'),
    path('codigo_marco/editar/<int:pk>', CodigoMarcoActualizar.as_view(), name='edit_codigo_marco'),

    path('tamanio/nuevo/', TamanioCrear.as_view(), name='nuevo_tamanio'),
    path('tamanio/listar/', views.tamanio_listar, name='list_tamanio'),
    path('tamanio/', TamanioListarAjaxListView.as_view(), name='tab_list_tamanio'),
    path('tamanio/editar/<int:pk>', TamanioActualizar.as_view(), name='edit_tamanio'),

    path('marco/nuevo/', MarcoCrear.as_view(), name='nuevo_marco'),
    path('marco/listar/', views.marco_listar, name='list_marco'),
    path('marco/', MarcoListarAjaxListView.as_view(), name='tab_list_marco'),
    path('marco/editar/<int:pk>', MarcoActualizar.as_view(), name='edit_marco'),

    path('marialuisa/nuevo/', MarialuisaCrear.as_view(), name='nuevo_marialuisa'),
    path('marialuisa/listar/', views.marialuisa_listar, name='list_marialuisa'),
    path('marialuisa/', MarialuisaAjaxListView.as_view(), name='tab_list_marialuisa'),
    path('marialuisa/editar/<int:pk>', MarialuisaActualizar.as_view(), name='edit_marialuisa'),

    path('modelomarialuisa/nuevo/', ModeloMarialuisaCrear.as_view(), name='nuevo_modelomarialuisa'),
    path('modelomarialuisa/listar/', views.modelomarialuisa_listar, name='list_modelomarialuisa'),
    path('modelomarialuisa/', ModeloMarialuisaAjaxListView.as_view(), name='tab_list_modelomarialuisa'),
    path('modelomarialuisa/editar/<int:pk>', ModeloMarialuisaActualizar.as_view(), name='edit_modelomarialuisa'),

]