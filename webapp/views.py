import math

import jwt
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout, update_session_auth_hash
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, DetailView
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse, HttpResponseForbidden

from config.conekta import agregar_tarjeta, actualizar_tarjeta, eliminar_tarjeta
from fotofertas.settings import KEY_FOTO, BASE_DIR
from webapp.forms import TarjetaForm, TarjetaEditForm, PerfilForm
from config.models import Fotografo, Rol, Fotografia, Direccion, Producto, Tarjeta, Descarga, Orden, Colonia, \
    SiguiendoFotografo, Usuario
from webapp.forms import RegistroForm, DireccionForm
from django_datatables_view.base_datatable_view import BaseDatatableView

def login(request):
    error_message = ''
    if request.user.is_authenticated:
        if request.user.rol.pk == 2:  # Administrador Fotofertas
            return redirect(reverse('administrador:list_marco'))
        elif request.user.rol.pk in [3,4]: # Cliente o Fotopartner
            return redirect(reverse('webapp:home'))
        logout(request)
    if request.method == 'POST':
        correo = request.POST['correo']
        password = request.POST['password']
        user = authenticate(correo=correo, password=password)
        if user is not None:
            if user.estatus:
                auth_login(request, user)
                if request.POST.get('next') is not None:
                    return redirect(request.POST.get('next'))
                elif user.rol.pk in [2,5]: # Administrador Fotofertas
                    return redirect(reverse('administrador:admin_menu'))
                elif user.rol.pk in [3,4]: # Cliente o Fotopartner
                    return redirect(reverse('webapp:home'))
                logout(request)
                return redirect(reverse('webapp:sitio_en_construccion'))
            else:
                error_message = "Usuario inactivo"
        else:
            error_message = "Usuario y/o contraseña incorrectos"
    context = {
        'error_message': error_message
    }
    if request.GET.get('next') is not None:
        context['next'] = request.GET.get('next')
    return render(request, 'config/login.html', context)

def logout_view(request):
    logout(request)
    return redirect(reverse('webapp:login'))

def index(request):
    template_name = 'fotopartner/index.html'
    return render(request, template_name)

def sitio_construccion(request):
    return render(request, 'config/sitio_en_construccion.html')

class ClienteRegistro(CreateView):

    model = Fotografo
    template_name = 'config/registro.html'
    success_url = '/webapp/login'
    form_class = RegistroForm

    def get_context_data(self, **kwargs):
        context = super(ClienteRegistro, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        return context

    def post(self, request, *args, **kwargs):

        if request.user.is_authenticated:
            if request.user.rol.pk == 2: # Si es administrador
                return redirect(reverse('administrador:list_marco'))
            else:
                logout_view(request)
                return redirect(reverse('webapp:login'))
        self.object = self.get_object

        rol = Rol.objects.get(pk=3) # Rol fotopartner

        form = self.form_class(request.POST)
        if form.is_valid():
            try:
                fotopartner = form.save(commit=False)
                fotopartner.rol = rol
                fotopartner.set_password(fotopartner.password)
                fotopartner.save()

                # Cosas para envio de correo
                # to = [user.correo]
                # ctx = {
                #     'token': token,
                #     'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode('UTF-8'),
                #     'user': user,
                #     'request': self.request,
                # }
                # message = get_template("mailing/correo_registro.html").render(ctx)
                # sendMail(to, 'Registro Fotofertas', message)
                user = authenticate(correo=fotopartner.correo, password=form.cleaned_data['password'])
                auth_login(request, user)
                return redirect(reverse('webapp:home'))
            except:
                return render(self.request, template_name=self.template_name,
                              context={'form': form,
                                       'error_message': 'Ocurrió un error en el registro, intenta mas tarde o con otro correo'})
        else:
            return self.render_to_response(self.get_context_data(form=form))


# Clase Direccion
class DireccionCrear(PermissionRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/webapp/login'
    permission_required = 'fotopartner'
    model = Direccion
    form_class = DireccionForm
    template_name = 'cliente/form_direccion.html'
    success_url = '/administrador/logo/listar'

    def get_context_data(self, **kwargs):
        context = super(DireccionCrear, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Registro de Dirección'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Completa todos los campos para registrar una dirección'
        return context

    def form_valid(self, form):
        direccion = form.save(commit=False)
        colonia= Colonia.objects.get(pk=form.data['colonia'])
        direccion.colonia= colonia
        direccion.usuario=self.request.user
        direccion.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('webapp:list_direccion')

@permission_required(perm='fotopartner', login_url='/webapp/login')
def direccion_listar(request):
    template_name = 'config/tab_base.html'
    context = {}
    context['titulo'] = 'Dirección'
    context['btn_nuevo'] = 'Agregar direccion'
    context['url_nuevo'] = reverse('webapp:nuevo_direccion')
    context['encabezados'] = [['Id', True],
                              ['Dirección', True],
                              ['Editar', False],
                              ['Estatus', True]]
    context['url_ajax'] = reverse('webapp:tab_list_direccion')
    context['url_update_estatus'] = '/webapp/direccion/cambiar_estatus/'

    return render(request, template_name, context)

class DireccionAjaxListView(PermissionRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/webapp/login'
    permission_required = 'fotopartner'
    model = Direccion
    columns = [
        'id', 'nombre', 'editar', 'estatus'
    ]

    order_columns = [
        'id', 'nombre', 'imagen', '', ''
    ]

    max_display_length = 100

    def render_column(self, row, column):
        if column == 'editar':
            return '<a class="" href ="' + reverse('webapp:edit_direccion',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><i class="far fa-edit"></i></a>'
        elif column == 'estatus':
            if row.estatus:
                return '<div class="custom-control custom-switch"><input type="checkbox" checked class="custom-control-input" onchange=cambiar_estatus(' + str(
                    row.pk) + ') id="customSwitch' + str(
                    row.pk) + '"><label class="custom-control-label" for="customSwitch' + str(
                    row.pk) + '">On</label></div>'
            else:
                return '<div class="custom-control custom-switch"><input type="checkbox" class="custom-control-input" onchange=cambiar_estatus(' + str(
                    row.pk) + ') id="customSwitch' + str(
                    row.pk) + '"><label class="custom-control-label" for="customSwitch' + str(
                    row.pk) + '">Off</label></div>'

        elif column == 'imagen':
                if row.imagen.url:
                    return '<img style="max-width: 170px; width:100%" src="'+ row.imagen.url +'" />'


        return super(DireccionAjaxListView, self).render_column(row, column)

    def get_initial_queryset(self):
        return Direccion.objects.filter(usuario=self.request.user)


class DireccionActualizar(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/webapp/login'
    permission_required = 'fotopartner'
    model = Direccion
    template_name = 'cliente/form_direccion.html'
    form_class = DireccionForm

    def get_context_data(self, **kwargs):
        context = super(DireccionActualizar, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Modificación de direccion'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Modifica los campos que requieras'
        return context

    def form_valid(self, form):
        # form.instance.set_password(form.cleaned_data['password'])
        direccion =form.save(commit=False)
        colonia = Colonia.objects.get(pk=form.data['colonia'])
        direccion.colonia = colonia
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('webapp:list_direccion')

@permission_required(perm='fotopartner', login_url='/webapp/login')
def direccion_cambiar_estatus(request, pk):
    direccion = get_object_or_404(Direccion, pk=pk)
    if direccion.estatus:
        direccion.estatus = False
    else:
        direccion.estatus = True
    direccion.save()
    return JsonResponse({'result': 0})
####



@permission_required(perm='fotopartner', login_url='/webapp/login')
def vista_perfil(request):
    template_name = 'cliente/perfil.html'
    fotografo = Fotografo.objects.get(pk=request.user.pk)
    fotografias = Fotografia.objects.filter(usuario__pk=fotografo.pk, estatus=True, aprobada=True,
                                            publica=True).order_by('fecha_alta')
    cant_fotos = len(fotografias)
    cant_siguiendo = SiguiendoFotografo.objects.filter(fotografo=fotografo).count()
    context = {'fotografo': fotografo, 'fotos': fotografias, 'cantidad_fotos': cant_fotos,
               'cant_siguiendo': cant_siguiendo}
    return render(request, template_name, context)

class ComprasAjaxListView(PermissionRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/webapp/login'
    permission_required = 'fotopartner'
    model = Producto
    columns = [
        'foto', 'foto_tamanio_precio.tamanio.nombre', 'tipo_compra.nombre', 'disponibles', 'descargar', 'subtotal', 'detalle'
    ]

    order_columns = [
    'foto.nombre', 'foto_tamanio_precio.tamanio.nombre', 'tipo_compra.nombre', '', '', 'subtotal', ''
    ]

    max_display_length = 100

    def render_column(self, row, column):

        if column == 'foto':
            return '<img style="width:35%; height:35%" src="' + row.foto.foto_home.url + '" />'
        elif column == 'disponibles':
            try:
                descarga = Descarga.objects.get(producto__pk=row.pk)
                return str(descarga.no_descargas_disponibles)
            except:
                return 'N/A'
        elif column == 'descargar':
            try:
                descarga = Descarga.objects.get(producto__pk=row.pk)
                if descarga.no_descargas_disponibles <=0:
                    return '<div class="button-a button-a-primary" style="background: #4c4c4c; border: none; font-family: sans-serif; font-size: 15px; line-height: 15px; text-decoration: none; padding: 15px 50px; color: #ffffff; display: block; border-radius: 4px;">Sin descargas</a>'
                return '<a download="fotofertas_prod_' + str(row.pk) + '.jpg" class="button-a button-a-primary" style="background: #12284C; border: none; font-family: sans-serif; font-size: 15px; line-height: 15px; text-decoration: none; padding: 15px 50px; color: #ffffff; display: block; border-radius: 4px;" href ="' + reverse(
                    'webapp:producto_descarga',
                    kwargs={
                        'token': descarga.token, 'image_name': 'fotofertas_prod_' + str(row.pk)}) + '">Descargar</a>'
            except:
                return 'N/A'
        elif column == 'detalle':
            return '<a class="" href ="' + reverse('webapp:detalle_orden',
                                                   kwargs={
                                                       'orden': row.orden.pk}) + '"><i class="fa fa-file-invoice" aria-hidden="true"></i></a>'

        return super(ComprasAjaxListView, self).render_column(row, column)

    def get_initial_queryset(self):
        return Producto.objects.filter(usuario=self.request.user, estatus_pago__pk=2)

@permission_required(perm='fotopartner', login_url='/webapp/login')
def detalle_orden(request, orden):
    template_name = 'cliente/detalle_orden.html'
    orden_objt = Orden.objects.get(pk=orden, estatus_compra__nombre='Ordenado')
    if orden_objt.usuario.pk == request.user.pk:
        productos = Producto.objects.filter(orden=orden_objt)
        return render(request, template_name, context={'orden':orden_objt, 'productos': productos})
    else:
        return HttpResponseForbidden()

@permission_required(perm='fotopartner', login_url='/webapp/login')
def vista_carrito(request):
    template_name = 'cliente/carrito.html'
    context = {}
    productos = Producto.objects.filter(usuario=request.user, orden__estatus_compra__pk=1)
    if productos.first():
        context['total'] = productos.first().total_orden
    else:
        context['total'] = 0.0
    return render(request, template_name, context)

def vista_foto(request, pk):
    foto = Fotografia.objects.get(pk=pk)
    template_name = 'cliente/foto.html'

    context = {
        'foto': foto
    }
    return render(request, template_name, context)

@permission_required(perm='fotopartner', login_url='/webapp/login')
def producto_descarga(request, token, image_name):
    context = {}
    template_error = 'cliente/error_descarga.html'
    try:
        decode_descarga = jwt.decode(token, KEY_FOTO, algorithm='HS256')
        print(decode_descarga)
        producto = Producto.objects.get(pk=decode_descarga['producto'])
        if producto.usuario.pk == request.user.pk:
            foto = Fotografia.objects.get(pk=producto.foto.pk)
            descarga = Descarga.objects.get(token=token, producto=producto, usuario=request.user)
            if descarga.no_descargas_disponibles > 0:
                with open('/var/django'+foto.foto_original.url, "rb") as f:
                    descarga.no_descargas_disponibles -= 1
                    descarga.save()
                    return HttpResponse(f.read(), content_type="image/jpeg")
            else:
                context['error'] = 'Sin descargas disponibles'
                return render(request, template_error, context)
        else:
            context['error'] = 'No puedes ver éste contenido'
            return render(request, template_error, context)
    except:
        context['error'] = 'El link no es válido'
    return render(request, template_error, context)


class EditarPerfil(UpdateView):
    redirect_field_name = 'next'
    login_url = '/webapp/login'
    permission_required = 'fotopartner'
    model = Usuario
    template_name = 'cliente/editar_perfil.html'
    form_class = PerfilForm

    def get_object(self):
        return Usuario.objects.get(pk=self.request.user.pk)  #

    def get_context_data(self, **kwargs):
        context = super(EditarPerfil, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Modificación de direccion'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Modifica los campos que requieras'
        return context

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('webapp:vista_editar_perfil')


def vista_marco(request, producto):
    template_name = 'cliente/marco.html'
    prod = Producto.objects.get(pk=producto)
    context = {'producto': prod}
    return render(request, template_name, context)

def vista_exclusivas(request):
    template_name = 'cliente/exclusivas.html'
    return render(request, template_name)

def vista_fotopartners(request):
    template_name = 'cliente/fotopartners.html'
    return render(request, template_name)

def vista_fotos_gratis(request):
    template_name = 'cliente/fotos_gratuitas.html'
    return render(request, template_name)

def vista_buscar_foto(request, categoria, nombre, tipo_foto, page):
    template_name = 'cliente/buscar_foto.html'
    queryset = Fotografia.objects.none()
    TAMANIO_PAGINA=20
    nombre = nombre
    categoria = categoria
    tipo_busqueda = tipo_foto
    if tipo_busqueda == 1:
        tipo_foto = 2 # Foto exclusiva
        template_name = 'cliente/buscar_foto.html'
    else:
        tipo_foto = 1 # Foto normal
        template_name = 'cliente/buscar_foto.html'
    if nombre is not 'None_Null':
        queryset = Fotografia.objects.filter(publica=True, aprobada=True, estatus=True, tipo_foto__pk=tipo_foto)
        queryset = queryset.filter(nombre__icontains=nombre) | queryset.filter(
            Q(etiquetas__nombre__icontains=nombre)) | queryset.filter(Q(categorias__nombre__icontains=nombre))
    if categoria is not 0:
        queryset = queryset.filter(categorias__pk=categoria, tipo_foto__pk=tipo_foto)
    start = page*TAMANIO_PAGINA
    fotos = queryset.distinct().order_by('-fecha_alta')[start: start+TAMANIO_PAGINA+1]
    num_fotos = len(fotos)
    paginas = math.ceil(num_fotos/TAMANIO_PAGINA)

    return render(request, template_name, context={'fotos': fotos, 'num_paginas': paginas})

def vista_otro_perfil(request, pk):
    template_name = 'cliente/otro_usuario.html'
    fotografo = Fotografo.objects.get(pk=pk)
    fotografias = Fotografia.objects.filter(usuario__pk=fotografo.pk, estatus=True, aprobada=True, publica=True).order_by('fecha_alta')
    cant_fotos = len(fotografias)
    cant_siguiendo = SiguiendoFotografo.objects.filter(fotografo=fotografo).count()
    context = {'fotografo': fotografo, 'fotos': fotografias, 'cantidad_fotos':cant_fotos, 'cant_siguiendo':cant_siguiendo}
    return render(request, template_name, context)

class TarjetaCrear(PermissionRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/webapp/login'
    permission_required = 'fotopartner'
    model = Tarjeta
    form_class = TarjetaForm
    template_name = 'cliente/tarjeta.html'

    def get_context_data(self, **kwargs):
        context = super(TarjetaCrear, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Registro de tarjeta'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Completa todos los campos para registrar una tarjeta'
        return context

    def form_valid(self, form):
        tarjeta_form = form.save(commit=False)
        source = agregar_tarjeta(self.request, form)
        if type(source) == str:
            return render(self.request, template_name=self.template_name,
                          context={'form': form, 'messages': [source]})
        tarjeta = Tarjeta.objects.create(usuario=self.request.user, ultimos_digitos=source.last4, token=source.id,
                          alias=tarjeta_form.alias, nombre_propietario=tarjeta_form.nombre_propietario)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('webapp:list_tarjeta')

@permission_required(perm='fotopartner', login_url='/webapp/login')
def tarjeta_listar(request):
    template_name = 'cliente/tab_tarjetas.html'
    context = {}
    context['titulo'] = 'Tarjetas'
    context['btn_nuevo'] = 'Agregar una tarjeta'
    context['url_nuevo'] = reverse('webapp:nuevo_tarjeta')
    context['encabezados'] = [['Propietario', True],
                              ['Alias', True],
                              ['Últimos digitos', True],
                              ['Editar', False],
                              ['Activar/Desactivar', True],
                              ['Eliminar', False]]
    context['url_ajax'] = reverse('webapp:tab_list_tarjeta')
    context['url_update_estatus'] = '/webapp/tarjeta/cambiar_estatus/'
    context['url_eliminar'] = '/webapp/tarjeta/eliminar/'
    return render(request, template_name, context)

class TarjetaAjaxListView(PermissionRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/webapp/login'
    permission_required = 'fotopartner'
    model = Tarjeta
    columns = [
        'nombre_propietario', 'alias', 'ultimos_digitos', 'editar', 'estatus', 'eliminar'
    ]

    order_columns = [
    'nombre_propietario', 'alias', 'ultimos_digitos', '', 'estatus', ''
    ]

    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('webapp:edit_tarjeta',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><i class="far fa-edit"></i></a>'
        elif column == 'eliminar':
            return '<a class="" href ="" onclick=eliminar(' + str(
                    row.pk) + ')><i class="fa fa-trash"></i></a>'
        elif column == 'estatus':
            if row.estatus:
                return '<div class="custom-control custom-switch"><input type="checkbox" checked class="custom-control-input" onchange=cambiar_estatus(' + str(
                    row.pk) + ') id="customSwitch' + str(
                    row.pk) + '"><label class="custom-control-label" for="customSwitch' + str(
                    row.pk) + '">On</label></div>'
            else:
                return '<div class="custom-control custom-switch"><input type="checkbox" class="custom-control-input" onchange=cambiar_estatus(' + str(
                    row.pk) + ') id="customSwitch' + str(
                    row.pk) + '"><label class="custom-control-label" for="customSwitch' + str(
                    row.pk) + '">Off</label></div>'

        return super(TarjetaAjaxListView, self).render_column(row, column)

    def get_initial_queryset(self):
        return Tarjeta.objects.filter(usuario=self.request.user, eliminado=False)


class TarjetaActualizar(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/webapp/login'
    permission_required = 'fotopartner'
    model = Tarjeta
    template_name = 'config/form_1col.html'
    form_class = TarjetaEditForm

    def get_context_data(self, **kwargs):
        context = super(TarjetaActualizar, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Modificación de tipo de papel'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Modifica los campos que requieras'
        return context

    def form_valid(self, form):
        id_tarjeta_conekta = form.instance.token
        resultado = actualizar_tarjeta(self.request, id_tarjeta_conekta)
        if type(resultado) == str:
            return render(self.request, template_name=self.template_name,
                          context={'form': form, 'messages': [resultado]})
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('webapp:list_tarjeta')

@permission_required(perm='fotopartner', login_url='/webapp/login')
def tarjeta_cambiar_estatus(request, pk):
    tarjeta = get_object_or_404(Tarjeta, pk=pk)
    if tarjeta.estatus:
        tarjeta.estatus = False
    else:
        tarjeta.estatus = True
    tarjeta.save()
    return JsonResponse({'result': 0})

@permission_required(perm='fotopartner', login_url='/webapp/login')
def tarjeta_eliminar(request, pk):
    tarjeta = get_object_or_404(Tarjeta, pk=pk)
    try:
        resultado = eliminar_tarjeta(request, tarjeta.token)
        if type(resultado) == str:
            return JsonResponse({'result': 1, 'error': resultado})
        tarjeta.delete()
    except:
        tarjeta.eliminado = True
        tarjeta.save()
    return JsonResponse({'result': 0})

@login_required(redirect_field_name='next', login_url='/webapp/login')
def cambiar_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Tu contraseña ha sido cambiada exitosamente')
            return redirect(reverse('webapp:cambiar_password'))
        else:
            messages.error(request, 'Por favor corrige el error mostrado.')
    else:
        form = PasswordChangeForm(request.user)
    titulo = 'Registro para cambiar tu contraseña'
    instrucciones = 'Ingresa tu contraseña actual y tu nueva contraseña que deseas'
    return render(request, 'config/form_1col.html',
                  {'form': form, 'titulo': titulo, 'instrucciones': instrucciones})