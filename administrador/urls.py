from django.urls import path

from administrador import views
from administrador.views import CodigoMarcoCrear, CodigoMarcoListarAjaxListView, CodigoMarcoActualizar, TamanioCrear, \
    TamanioListarAjaxListView, TamanioActualizar, MarcoCrear, MarcoListarAjaxListView, MarcoActualizar, MarialuisaCrear, \
    MarialuisaAjaxListView, MarialuisaActualizar, ModeloMarialuisaCrear, ModeloMarialuisaAjaxListView, \
    ModeloMarialuisaActualizar, TexturaCrear, TexturaAjaxListView, TexturaActualizar, LogoCrear, \
    LogoAjaxListView, LogoActualizar, PersonalAdministrativoCrear, PersonalAdministrativoAjaxListView, \
    PersonalAdministrativoActualizar, VentasAjaxListView, MenuFotopartnerCrear, MenuFotopartnerAjaxListView, \
    MenuFotopartnerActualizar, PromocionCrear, PromocionAjaxListView, PromocionActualizar, \
    UsuariosGeneralesAjaxListView, FotopartnersAjaxListView, UsuariosBloqueadosAjaxListView, AprobarFotoAjaxListView, \
    TipoPapelCrear, TipoPapelAjaxListView, TipoPapelActualizar, PapelImpresionCrear, PapelImpresionAjaxListView, \
    PapelImpresionActualizar, HistorialVentasAjaxListView, ContactanosListarAjaxListView, ContactanosActualizar, \
    CategoriaCrear, CategoriaAjaxListView, CategoriaActualizar

app_name = 'administrador'
urlpatterns = [

    # Este no sirve
    path('codigo_marco/nuevo/', CodigoMarcoCrear.as_view(), name='nuevo_codigo_marco'),
    path('codigo_marco/listar/', views.codigo_marco_listar, name='list_codigo_marco'),
    path('tabla_codigo_marco/', CodigoMarcoListarAjaxListView.as_view(), name='tab_list_codigo_marco'),
    path('codigo_marco/editar/<int:pk>', CodigoMarcoActualizar.as_view(), name='edit_codigo_marco'),

    path('tamanio/nuevo/', TamanioCrear.as_view(), name='nuevo_tamanio'),
    path('tamanio/listar/', views.tamanio_listar, name='list_tamanio'),
    path('tamanio/', TamanioListarAjaxListView.as_view(), name='tab_list_tamanio'),
    path('tamanio/editar/<int:pk>', TamanioActualizar.as_view(), name='edit_tamanio'),
    path('tamanio/cambiar_estatus/<int:pk>', views.tamanio_cambiar_estatus,
         name='tamanio_cambiar_estatus'),

    path('marco/nuevo/', MarcoCrear.as_view(), name='nuevo_marco'),
    path('marco/listar/', views.marco_listar, name='list_marco'),
    path('marco/', MarcoListarAjaxListView.as_view(), name='tab_list_marco'),
    path('marco/editar/<int:pk>', MarcoActualizar.as_view(), name='edit_marco'),
    path('marco/cambiar_estatus/<int:pk>', views.marco_cambiar_estatus,
         name='marco_cambiar_estatus'),

    path('marialuisa/nuevo/', MarialuisaCrear.as_view(), name='nuevo_marialuisa'),
    path('marialuisa/listar/', views.marialuisa_listar, name='list_marialuisa'),
    path('marialuisa/', MarialuisaAjaxListView.as_view(), name='tab_list_marialuisa'),
    path('marialuisa/editar/<int:pk>', MarialuisaActualizar.as_view(), name='edit_marialuisa'),
    path('marialuisa/cambiar_estatus/<int:pk>', views.marialuisa_cambiar_estatus,
         name='marialuisa_cambiar_estatus'),

    path('modelomarialuisa/nuevo/', ModeloMarialuisaCrear.as_view(), name='nuevo_modelomarialuisa'),
    path('modelomarialuisa/listar/', views.modelomarialuisa_listar, name='list_modelomarialuisa'),
    path('modelomarialuisa/', ModeloMarialuisaAjaxListView.as_view(), name='tab_list_modelomarialuisa'),
    path('modelomarialuisa/editar/<int:pk>', ModeloMarialuisaActualizar.as_view(), name='edit_modelomarialuisa'),
    path('modelomarialuisa/cambiar_estatus/<int:pk>', views.modelomarialuisa_cambiar_estatus,
         name='modelomarialuisa_cambiar_estatus'),


    path('papel_impresion/nuevo/', PapelImpresionCrear.as_view(), name='nuevo_papel_impresion'),
    path('papel_impresion/listar/', views.papel_impresion_listar, name='list_papel_impresion'),
    path('papel_impresion/', PapelImpresionAjaxListView.as_view(), name='tab_list_papel_impresion'),
    path('papel_impresion/editar/<int:pk>', PapelImpresionActualizar.as_view(), name='edit_papel_impresion'),
    path('papel_impresion/cambiar_estatus/<int:pk>', views.papel_impresion_cambiar_estatus, name='papel_impresion_cambiar_estatus'),

    path('textura/nuevo/', TexturaCrear.as_view(), name='nuevo_textura'),
    path('textura/listar/', views.textura_listar, name='list_textura'),
    path('textura/', TexturaAjaxListView.as_view(), name='tab_list_textura'),
    path('textura/editar/<int:pk>', TexturaActualizar.as_view(), name='edit_textura'),
    path('textura/cambiar_estatus/<int:pk>', views.textura_cambiar_estatus,
         name='textura_cambiar_estatus'),

    path('logo/nuevo/', LogoCrear.as_view(), name='nuevo_logo'),
    path('logo/listar/', views.logo_listar, name='list_logo'),
    path('logo/', LogoAjaxListView.as_view(), name='tab_list_logo'),
    path('logo/editar/<int:pk>', LogoActualizar.as_view(), name='edit_logo'),
    path('logo/cambiar_estatus/<int:pk>', views.logo_cambiar_estatus,
         name='logo_cambiar_estatus'),

    path('MenuFotopartner/nuevo/', MenuFotopartnerCrear.as_view(), name='nuevo_MenuFotopartner'),
    path('MenuFotopartner/listar/', views.MenuFotopartner_listar, name='list_MenuFotopartner'),
    path('MenuFotopartner/', MenuFotopartnerAjaxListView.as_view(), name='tab_list_MenuFotopartner'),
    path('MenuFotopartner/editar/<int:pk>', MenuFotopartnerActualizar.as_view(), name='edit_MenuFotopartner'),
    path('MenuFotopartner/cambiar_estatus/<int:pk>', views.MenuFotopartner_cambiar_estatus,
         name='MenuFotopartner_cambiar_estatus'),

    path('Promocion/nuevo/', PromocionCrear.as_view(), name='nuevo_Promocion'),
    path('Promocion/listar/', views.Promocion_listar, name='list_Promocion'),
    path('Promocion/', PromocionAjaxListView.as_view(), name='tab_list_Promocion'),
    path('Promocion/editar/<int:pk>', PromocionActualizar.as_view(), name='edit_Promocion'),
    path('Promocion/cambiar_estatus/<int:pk>', views.Promocion_cambiar_estatus,
         name='Promocion_cambiar_estatus'),
 
    path('categoria/nuevo/', CategoriaCrear.as_view(), name='nuevo_categoria'),
    path('categoria/listar/', views.Categoria_listar, name='list_categoria'),
    path('categoria/', CategoriaAjaxListView.as_view(), name='tab_list_categoria'),
    path('categoria/editar/<int:pk>', CategoriaActualizar.as_view(), name='edit_categoria'),
    path('categoria/cambiar_estatus/<int:pk>', views.Categoria_cambiar_estatus,
         name='Categoria_cambiar_estatus'),

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

    path('historial_ventas/listar/', views.historial_ventas_listar, name='list_historial_ventas'),
    path('historial_ventas/ajax/', HistorialVentasAjaxListView.as_view(), name='tab_list_historial_ventas'),

    path('fotografo/cambiar_estatus/<int:pk>', views.fotografo_cambiar_estatus, name='cambiar_estatus_fotografo'),
    path('fotografo/cambiar_confiable/<int:pk>', views.fotografo_cambiar_confiable, name='fotografo_cambiar_confiable'),

    path('usuarios_generales/listar/', views.usuarios_generales_listar, name='list_usuarios_generales'),
    path('usuarios_generales/ajax/', UsuariosGeneralesAjaxListView.as_view(), name='tab_list_usuarios_generales'),

    path('fotopartners/listar/', views.fotopartners_listar, name='list_fotopartners'),
    path('fotopartners/ajax/', FotopartnersAjaxListView.as_view(), name='tab_list_fotopartners'),

    path('usuarios_bloqueados/listar/', views.usuarios_bloqueados_listar, name='list_usuarios_bloqueados'),
    path('usuarios_bloqueados/ajax/', UsuariosBloqueadosAjaxListView.as_view(), name='tab_list_usuarios_bloqueados'),

    path('aprobar_foto/listar/', views.aprobar_foto_listar, name='list_aprobar_foto'),
    path('aprobar_foto/ajax/', AprobarFotoAjaxListView.as_view(), name='tab_list_aprobar_foto'),

    path('tipo_papel/nuevo/', TipoPapelCrear.as_view(), name='nuevo_tipo_papel'),
    path('tipo_papel/listar/', views.tipo_papel_listar, name='list_tipo_papel'),
    path('tipo_papel/', TipoPapelAjaxListView.as_view(), name='tab_list_tipo_papel'),
    path('tipo_papel/editar/<int:pk>', TipoPapelActualizar.as_view(), name='edit_tipo_papel'),
    path('tipo_papel/cambiar_estatus/<int:pk>', views.tipo_papel_cambiar_estatus, name='cambiar_estatus_tipo_papel'),

    path('contactanos/listar/', views.contactanos_listar, name='list_contactanos'),
    path('tabla_contactanos/', ContactanosListarAjaxListView.as_view(), name='tab_list_contactanos'),
    path('contactanos/editar/<int:pk>', ContactanosActualizar.as_view(), name='edit_contactanos'),
]