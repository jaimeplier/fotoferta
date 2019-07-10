from django.urls import path

from administrador import views
from administrador.views import CodigoMarcoCrear, CodigoMarcoListarAjaxListView, CodigoMarcoActualizar, TamanioCrear, \
    TamanioListarAjaxListView, TamanioActualizar, MarcoCrear, MarcoListarAjaxListView, MarcoActualizar, MarialuisaCrear, \
    MarialuisaAjaxListView, MarialuisaActualizar, ModeloMarialuisaCrear, ModeloMarialuisaAjaxListView, \
    ModeloMarialuisaActualizar, GrosorPapelCrear, GrosorPapelAjaxListView, GrosorPapelActualizar, TipoPapelCrear, \
    TipoPapelAjaxListView, TipoPapelActualizar, TexturaCrear, TexturaAjaxListView, TexturaActualizar, LogoCrear, \
    LogoAjaxListView, LogoActualizar, PersonalAdministrativoCrear, PersonalAdministrativoAjaxListView, \
    PersonalAdministrativoActualizar, VentasAjaxListView, MenuFotopartnerCrear, MenuFotopartnerAjaxListView, \
    MenuFotopartnerActualizar, PromocionCrear, PromocionAjaxListView, PromocionActualizar, \
    UsuariosGeneralesAjaxListView, FotopartnersAjaxListView

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

    path('grosor_papel/nuevo/', GrosorPapelCrear.as_view(), name='nuevo_grosor_papel'),
    path('grosor_papel/listar/', views.grosor_papel_listar, name='list_grosor_papel'),
    path('grosor_papel/', GrosorPapelAjaxListView.as_view(), name='tab_list_grosor_papel'),
    path('grosor_papel/editar/<int:pk>', GrosorPapelActualizar.as_view(), name='edit_grosor_papel'),

    path('tipo_papel/nuevo/', TipoPapelCrear.as_view(), name='nuevo_tipo_papel'),
    path('tipo_papel/listar/', views.tipo_papel_listar, name='list_tipo_papel'),
    path('tipo_papel/', TipoPapelAjaxListView.as_view(), name='tab_list_tipo_papel'),
    path('tipo_papel/editar/<int:pk>', TipoPapelActualizar.as_view(), name='edit_tipo_papel'),

    path('textura/nuevo/', TexturaCrear.as_view(), name='nuevo_textura'),
    path('textura/listar/', views.textura_listar, name='list_textura'),
    path('textura/', TexturaAjaxListView.as_view(), name='tab_list_textura'),
    path('textura/editar/<int:pk>', TexturaActualizar.as_view(), name='edit_textura'),

    path('logo/nuevo/', LogoCrear.as_view(), name='nuevo_logo'),
    path('logo/listar/', views.logo_listar, name='list_logo'),
    path('logo/', LogoAjaxListView.as_view(), name='tab_list_logo'),
    path('logo/editar/<int:pk>', LogoActualizar.as_view(), name='edit_logo'),

    path('MenuFotopartner/nuevo/', MenuFotopartnerCrear.as_view(), name='nuevo_MenuFotopartner'),
    path('MenuFotopartner/listar/', views.MenuFotopartner_listar, name='list_MenuFotopartner'),
    path('MenuFotopartner/', MenuFotopartnerAjaxListView.as_view(), name='tab_list_MenuFotopartner'),
    path('MenuFotopartner/editar/<int:pk>', MenuFotopartnerActualizar.as_view(), name='edit_MenuFotopartner'),

    path('Promocion/nuevo/', PromocionCrear.as_view(), name='nuevo_Promocion'),
    path('Promocion/listar/', views.Promocion_listar, name='list_Promocion'),
    path('Promocion/', PromocionAjaxListView.as_view(), name='tab_list_Promocion'),
    path('Promocion/editar/<int:pk>', PromocionActualizar.as_view(), name='edit_Promocion'),

    path('personal_administrativo/nuevo/', PersonalAdministrativoCrear.as_view(), name='nuevo_personal_administrativo'),
    path('personal_administrativo/listar/', views.personal_administrativo_listar, name='list_personal_administrativo'),
    path('personal_administrativo/ajax/', PersonalAdministrativoAjaxListView.as_view(),
         name='tab_list_personal_administrativo'),
    path('personal_administrativo/editar/<int:pk>', PersonalAdministrativoActualizar.as_view(),
         name='edit_personal_administrativo'),
    path('personal_administrativo/cambiar_estatus/<int:pk>', views.personal_administrativo_cambiar_estatus,
         name='cambiar_estatus_personal_administrativo'),

    path('ventas/listar/', views.ventas_listar, name='list_ventas'),
    path('ventas/ajax/', VentasAjaxListView.as_view(), name='tab_list_ventas'),

    path('fotografo/cambiar_estatus/<int:pk>', views.fotografo_cambiar_estatus, name='cambiar_estatus_fotografo'),

    path('usuarios_generales/listar/', views.usuarios_generales_listar, name='list_usuarios_generales'),
    path('usuarios_generales/ajax/', UsuariosGeneralesAjaxListView.as_view(), name='tab_list_usuarios_generales'),

    path('fotopartners/listar/', views.fotopartners_listar, name='list_fotopartners'),
    path('fotopartners/ajax/', FotopartnersAjaxListView.as_view(), name='tab_list_fotopartners'),

]
