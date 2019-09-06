import jwt
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
# Create your views here.
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, DetailView
from pytz import timezone

from administrador.forms import CodigoMarcoForm, MarcoForm, MarialuisaForm, TamanioForm, ModeloMarialuisaForm, \
    TexturaForm, LogoForm, PersonalAdministrativoForm, MenuFotopartnerForm, \
    PromocionForm, TipoPapelForm, PapelImpresionForm, ContactanosForm, CategoriaForm, FotoPrecioForm
from config.models import CodigoMarco, Marco, MariaLuisa, ModeloMariaLuisa, Tamanio, Textura, \
    Logo, PersonalAdministrativo, Rol, Orden, MenuFotopartner, Promocion, Fotografo, Fotografia, TipoPapel, \
    PapelImpresion, Contactanos, Categoria, FotoPrecio, Producto, Descarga, EstatusCompra
from django_datatables_view.base_datatable_view import BaseDatatableView

from fotofertas import settings

### No tocar, codigo marco -> muerto
from fotofertas.settings import KEY_FOTO


class CodigoMarcoCrear(PermissionRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/webapp/login'
    permission_required = 'administrador'
    model = CodigoMarco
    form_class = CodigoMarcoForm
    template_name = 'config/form_1col.html'
    success_url = '/administrador/codigo_marco/nuevo'

    def get_context_data(self, **kwargs):
        context = super(CodigoMarcoCrear, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Registro de código de marco'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Completa todos los campos para registrar un personal de callcenter'
        return context

    def form_valid(self, form):
        codigo_marco = form.save(commit=False)
        codigo_marco.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('administrador:list_codigo_marco')



@permission_required(perm='administrador', login_url='/webapp/login')
def codigo_marco_listar(request):
    template_name = 'config/tab_base.html'
    context = {}
    context['titulo'] = 'Código marco'
    context['btn_nuevo'] = 'Agregar código'
    context['url_nuevo'] = reverse('administrador:nuevo_codigo_marco')
    context['encabezados'] = [['Nombre', True],
                              ['Correo', True],
                              ['Editar', False],
                              ['Estatus', True]]
    context['url_ajax'] = reverse('administrador:tab_list_codigo_marco')
    context['url_update_estatus'] = '/administrador/codigo_marco/cambiar_estatus/'


    return render(request, template_name, context)

class CodigoMarcoListarAjaxListView(PermissionRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/webapp/login'
    permission_required = 'administrador'
    model = CodigoMarco
    columns = ['id', 'codigo', 'editar', 'estatus']
    order_columns = ['id', 'codigo', '', '']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('administrador:edit_codigo_marco',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><i class="far fa-edit"></i></a>'

        elif column == 'estatus':
            if row.estatus:
                return '<div class="custom-control custom-switch"><input type="checkbox" checked class="custom-control-input" onchange=cambiar_estatus(' + str(
                    row.pk) + ') id="customSwitch'+str(row.pk)+'"><label class="custom-control-label" for="customSwitch'+str(row.pk)+'">On</label></div>'
            else:
                return '<div class="custom-control custom-switch"><input type="checkbox" class="custom-control-input" onchange=cambiar_estatus(' + str(
                    row.pk) + ') id="customSwitch'+str(row.pk)+'"><label class="custom-control-label" for="customSwitch'+str(row.pk)+'">Off</label></div>'

        return super(CodigoMarcoListarAjaxListView, self).render_column(row, column)

    def get_initial_queryset(self):
        return CodigoMarco.objects.all()

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(codigo__icontains=search) | qs.filter(id__icontains=search)
        return qs


class CodigoMarcoActualizar(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/webapp/login'
    permission_required = 'administrador'
    model = CodigoMarco
    template_name = 'config/form_1col.html'
    form_class = CodigoMarcoForm

    def get_context_data(self, **kwargs):
        context = super(CodigoMarcoActualizar, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Modificación de código de marco'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Modifica los campos que requieras'
        return context

    def form_valid(self, form):
        # form.instance.set_password(form.cleaned_data['password'])
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('administrador:list_codigo_marco')


   # Clase Tamaño

class TamanioCrear(PermissionRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/webapp/login'
    permission_required = 'administrador'
    model = Tamanio
    form_class = TamanioForm
    template_name = 'config/form_1col.html'
    success_url = '/administrador/tamanio/nuevo'

    def get_context_data(self, **kwargs):
        context = super(TamanioCrear, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Registro de tamaño'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Completa todos los campos para registrar un tamaño'
        return context

    def form_valid(self, form):
        tamanio = form.save(commit=False)
        tamanio.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('administrador:list_tamanio')

@permission_required(perm='administrador', login_url='/webapp/login')
def tamanio_listar(request):
    template_name = 'config/tab_base.html'
    context = {}
    context['titulo'] = 'Tamaño'
    context['btn_nuevo'] = 'Agregar tamaño'
    context['url_nuevo'] = reverse('administrador:nuevo_tamanio')
    context['encabezados'] = [['Id', True],
                              ['Nombre', True],
                              ['Editar', False],
                              ['Estatus', True]]
    context['url_ajax'] = reverse('administrador:tab_list_tamanio')
    context['url_update_estatus'] = '/administrador/tamanio/cambiar_estatus/'


    return render(request, template_name, context)

class TamanioListarAjaxListView(PermissionRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/webapp/login'
    permission_required = 'administrador'
    model = Tamanio
    columns = ['id', 'nombre', 'editar', 'estatus']
    order_columns = ['id', 'nombre', '', '']
    max_display_length = 100

    def render_column(self, row, column):
        if column == 'editar':
            return '<a class="" href ="' + reverse('administrador:edit_tamanio',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><i class="far fa-edit"></i></a>'

        elif column == 'estatus':
            if row.estatus:
                return '<div class="custom-control custom-switch"><input type="checkbox" checked class="custom-control-input" onchange=cambiar_estatus(' + str(
                    row.pk) + ') id="customSwitch'+str(row.pk)+'"><label class="custom-control-label" for="customSwitch'+str(row.pk)+'">On</label></div>'
            else:
                return '<div class="custom-control custom-switch"><input type="checkbox" class="custom-control-input" onchange=cambiar_estatus(' + str(
                    row.pk) + ') id="customSwitch'+str(row.pk)+'"><label class="custom-control-label" for="customSwitch'+str(row.pk)+'">Off</label></div>'

        return super(TamanioListarAjaxListView, self).render_column(row, column)

    def get_initial_queryset(self):
        return Tamanio.objects.all()

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(nombre__icontains=search) | qs.filter(id__icontains=search)
        return qs

class TamanioActualizar(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/webapp/login'
    permission_required = 'administrador'
    model = Tamanio
    template_name = 'config/form_1col.html'
    form_class = TamanioForm

    def get_context_data(self, **kwargs):
        context = super(TamanioActualizar, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Modificación de tamaño'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Modifica los campos que requieras'
        return context

    def form_valid(self, form):
        # form.instance.set_password(form.cleaned_data['password'])
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('administrador:list_tamanio')

@permission_required(perm='administrador', login_url='/webapp/login')
def tamanio_cambiar_estatus(request, pk):
    tamanio = get_object_or_404(Tamanio, pk=pk)
    if tamanio.estatus:
        tamanio.estatus = False
    else:
        tamanio.estatus = True
    tamanio.save()
    return JsonResponse({'result': 0})

# Clase Marco

class MarcoCrear(PermissionRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/webapp/login'
    permission_required = 'administrador'
    model = Marco
    form_class = MarcoForm
    template_name = 'config/form_1col.html'
    success_url = '/administrador/marco/nuevo'

    def get_context_data(self, **kwargs):
        context = super(MarcoCrear, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Registro de marco'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Completa todos los campos para registrar un marco'
        return context

    def form_valid(self, form):
        tamanio = form.save(commit=False)
        tamanio.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('administrador:list_marco')

@permission_required(perm='administrador', login_url='/webapp/login')
def marco_listar(request):
    template_name = 'config/tab_base.html'
    context = {}
    context['titulo'] = 'Marco'
    context['btn_nuevo'] = 'Agregar marco'
    context['url_nuevo'] = reverse('administrador:nuevo_marco')
    context['encabezados'] = [['Id', True],
                              ['Nombre', True],
                              ['Código', True],
                              ['Tamaño', True],
                              ['Alto', True],
                              ['Ancho', True],
                              ['Grosor lateral', True],
                              ['Grosor total', True],
                              ['Grosor final', True],
                              ['Profundidad', True],
                              ['Peso', True],
                              ['Precio', True],
                              ['Imagen horizontal', True],
                              ['Imagen vertical', True],
                              ['Editar', False],
                              ['Estatus', True]]
    context['url_ajax'] = reverse('administrador:tab_list_marco')
    context['url_update_estatus'] = '/administrador/marco/cambiar_estatus/'

    return render(request, template_name, context)

class MarcoListarAjaxListView(PermissionRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/webapp/login'
    permission_required = 'administrador'
    model = Tamanio
    columns = [
        'id', 'nombre', 'codigo', 'tamanio', 'alto', 'ancho','grosor_lado','grosor_total', 'grosor_final', 'profundidad', 'peso', 'precio',
        'imagen_horizontal', 'imagen_vertical','editar', 'estatus']

    order_columns = ['id', 'nombre', 'codigo', 'tamanio', 'alto', 'ancho','grosor_lado','grosor_total', 'grosor_final', 'profundidad', 'peso', 'precio',
        'imagen_horizontal', 'imagen_vertical', '', '']

    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('administrador:edit_marco',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><i class="far fa-edit"></i></a>'
        elif column == 'imagen_horizontal':
            if row.imagen_horizontal.url:
                return '<img style="width:100%" src="'+ row.imagen_horizontal.url +'" />'
        elif column == 'imagen_vertical':
            if row.imagen_vertical.url:
                return '<img style="width:100%" src="'+ row.imagen_vertical.url +'" />'

        elif column == 'precio':
            return "${0:,.2f}".format(row.precio)

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

        return super(MarcoListarAjaxListView, self).render_column(row, column)

    def get_initial_queryset(self):
        return Marco.objects.all()
        
    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(nombre__icontains=search) | qs.filter(id__icontains=search) | qs.filter(codigo__icontains=search) | qs.filter(tamanio__nombre__icontains=search) \
                # qs.filter(tamanio__icontains=search) | qs.filter(alto__icontains=search) | qs.filter(ancho__icontains=search) | \
                # qs.filter(grosor_lado__icontains=search) | qs.filter(grosor_total__icontains=search) | qs.filter(grosor_final__icontains=search) | \
                # qs.filter(profundidad__icontains=search) | qs.filter(peso__icontains=search) | qs.filter(precio__icontains=search) | \
                # qs.filter(imagen_horizontal__icontains=search) | qs.filter(imagen_vertical__icontains=search)
        return qs


class MarcoActualizar(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/webapp/login'
    permission_required = 'administrador'
    model = Marco
    template_name = 'config/form_1col.html'
    form_class = MarcoForm

    def get_context_data(self, **kwargs):
        context = super(MarcoActualizar, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Modificación de marco'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Modifica los campos que requieras'
        return context

    def form_valid(self, form):
        # form.instance.set_password(form.cleaned_data['password'])
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('administrador:list_marco')

@permission_required(perm='administrador', login_url='/webapp/login')
def marco_cambiar_estatus(request, pk):
    marco = get_object_or_404(Marco, pk=pk)
    if marco.estatus:
        marco.estatus = False
    else:
        marco.estatus = True
    marco.save()
    return JsonResponse({'result': 0})


# Modelo Marialuisa
class ModeloMarialuisaCrear(PermissionRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/webapp/login'
    permission_required = 'administrador'
    model = ModeloMariaLuisa
    form_class = ModeloMarialuisaForm
    template_name = 'config/form_1col.html'
    success_url = '/administrador/modelomarialuisa/nuevo'

    def get_context_data(self, **kwargs):
        context = super(ModeloMarialuisaCrear, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Registro de modelo de marialuisa'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Completa todos los campos para registrar un modelo de marialuisa'
        return context

    def form_valid(self, form):
        maluisa = form.save(commit=False)
        maluisa.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('administrador:list_modelomarialuisa')

@permission_required(perm='administrador', login_url='/webapp/login')
def modelomarialuisa_listar(request):
    template_name = 'config/tab_base.html'
    context = {}
    context['titulo'] = 'Modelos de Marialuisa'
    context['btn_nuevo'] = 'Agregar modelo marialuisa'
    context['url_nuevo'] = reverse('administrador:nuevo_modelomarialuisa')
    context['encabezados'] = [['Id', True],
                              ['Nombre', True],
                              ['Editar', False],
                              ['Estatus', False],
                              ]
    context['url_ajax'] = reverse('administrador:tab_list_modelomarialuisa')
    context['url_update_estatus'] = '/administrador/modelomarialuisa/cambiar_estatus/'


    return render(request, template_name, context)

class ModeloMarialuisaAjaxListView(PermissionRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/webapp/login'
    permission_required = 'administrador'
    model = ModeloMariaLuisa
    columns = [
        'id', 'modelo', 'editar', 'estatus'
    ]

    order_columns = [
        'id','modelo', '', 'estatus'
    ]

    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('administrador:edit_modelomarialuisa',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><i class="far fa-edit"></i></a>'
        elif column == 'estatus':
            if row.estatus:
                return '<div class="custom-control custom-switch"><input type="checkbox" checked class="custom-control-input" onchange=cambiar_estatus(' + str(
                    row.pk) + ') id="customSwitch'+str(row.pk)+'"><label class="custom-control-label" for="customSwitch'+str(row.pk)+'">On</label></div>'
            else:
                return '<div class="custom-control custom-switch"><input type="checkbox" class="custom-control-input" onchange=cambiar_estatus(' + str(
                    row.pk) + ') id="customSwitch'+str(row.pk)+'"><label class="custom-control-label" for="customSwitch'+str(row.pk)+'">Off</label></div>'

        return super(ModeloMarialuisaAjaxListView, self).render_column(row, column)

    def get_initial_queryset(self):
        return ModeloMariaLuisa.objects.all()

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(modelo__icontains=search) | qs.filter(id__icontains=search)
        return qs

class ModeloMarialuisaActualizar(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/webapp/login'
    permission_required = 'administrador'
    model = ModeloMariaLuisa
    template_name = 'config/form_1col.html'
    form_class = ModeloMarialuisaForm

    def get_context_data(self, **kwargs):
        context = super(ModeloMarialuisaActualizar, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Modificación del modelo de maria luisa'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Modifica los campos que requieras'
        return context

    def form_valid(self, form):
        # form.instance.set_password(form.cleaned_data['password'])
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('administrador:list_modelomarialuisa')

@permission_required(perm='administrador', login_url='/webapp/login')
def modelomarialuisa_cambiar_estatus(request, pk):
    modelomarialuisa = get_object_or_404(Marco, pk=pk)
    if modelomarialuisa.estatus:
        modelomarialuisa.estatus = False
    else:
        modelomarialuisa.estatus = True
    modelomarialuisa.save()
    return JsonResponse({'result': 0})

# Clase Marialuisa
class MarialuisaCrear(PermissionRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/webapp/login'
    permission_required = 'administrador'
    model = MariaLuisa
    form_class = MarialuisaForm
    template_name = 'config/form_1col.html'
    success_url = '/administrador/marialuisa/listar'

    def get_context_data(self, **kwargs):
        context = super(MarialuisaCrear, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Registro de Marialuisa'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Completa todos los campos para registrar una marialuisa'
        return context

    def form_valid(self, form):
        maluisa = form.save(commit=False)
        maluisa.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('administrador:list_marialuisa')

@permission_required(perm='administrador', login_url='/webapp/login')
def marialuisa_listar(request):
    template_name = 'config/tab_base.html'
    context = {}
    context['titulo'] = 'Marialuisa'
    context['btn_nuevo'] = 'Agregar marialuisa'
    context['url_nuevo'] = reverse('administrador:nuevo_marialuisa')
    context['encabezados'] = [['Nombre', True],
                              ['Modelo', True],
                              ['Precio', True],
                              ['Tamaño', True],
                              ['Imagen', True],
                              ['Editar', False],
                              ['Estatus', True]]
    context['url_ajax'] = reverse('administrador:tab_list_marialuisa')
    context['url_update_estatus'] = '/administrador/marialuisa/cambiar_estatus/'

    return render(request, template_name, context)

class MarialuisaAjaxListView(PermissionRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/webapp/login'
    permission_required = 'administrador'
    model = MariaLuisa
    columns = [
        'nombre','modelo.nombre', 'precio', 'tamanio', 'imagen', 'editar', 'estatus'
    ]

    order_columns = [
    'nombre', 'modelo.nombre', 'precio', 'tamanio', 'imagen', '', ''
    ]

    max_display_length = 100

    def render_column(self, row, column):
        if column == 'editar':
            return '<a class="" href ="' + reverse('administrador:edit_marialuisa',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><i class="far fa-edit"></i></a>'
        elif column == 'estatus':
            if row.estatus:
                return '<div class="custom-control custom-switch"><input type="checkbox" checked class="custom-control-input" onchange=cambiar_estatus(' + str(
                    row.pk) + ') id="customSwitch'+str(row.pk)+'"><label class="custom-control-label" for="customSwitch'+str(row.pk)+'">On</label></div>'
            else:
                return '<div class="custom-control custom-switch"><input type="checkbox" class="custom-control-input" onchange=cambiar_estatus(' + str(
                    row.pk) + ') id="customSwitch'+str(row.pk)+'"><label class="custom-control-label" for="customSwitch'+str(row.pk)+'">Off</label></div>'

        elif column == 'precio':
            return "${0:,.2f}".format(row.precio)



        elif column == 'imagen':
                if row.imagen.url:
                    return '<img style="width:100%" src="'+ row.imagen.url +'" />'


        return super(MarialuisaAjaxListView, self).render_column(row, column)

    def get_initial_queryset(self):
        return MariaLuisa.objects.all()

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(nombre__icontains=search) | qs.filter(tamanio__icontains=search) | qs.filter(precio__icontains=search)
        return qs

class MarialuisaActualizar(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/webapp/login'
    permission_required = 'administrador'
    model = MariaLuisa
    template_name = 'config/form_1col.html'
    form_class = MarialuisaForm

    def get_context_data(self, **kwargs):
        context = super(MarialuisaActualizar, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Modificación de Marialuisa'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Modifica los campos que requieras'
        return context

    def form_valid(self, form):
        # form.instance.set_password(form.cleaned_data['password'])
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('administrador:list_marialuisa')

@permission_required(perm='administrador', login_url='/webapp/login')
def marialuisa_cambiar_estatus(request, pk):
    marialuisa = get_object_or_404(MariaLuisa, pk=pk)
    if marialuisa.estatus:
        marialuisa.estatus = False
    else:
        marialuisa.estatus = True
    marialuisa.save()
    return JsonResponse({'result': 0})

# Clase TipoPapel
class TipoPapelCrear(PermissionRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/webapp/login'
    permission_required = 'administrador'
    model = TipoPapel
    form_class = TipoPapelForm
    template_name = 'config/form_1col.html'
    success_url = '/administrador/tipo_papel/listar'

    def get_context_data(self, **kwargs):
        context = super(TipoPapelCrear, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Registro de tipo de papel'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Completa todos los campos para registrar un tipo de papel'
        return context

    def form_valid(self, form):
        tipo_papel = form.save(commit=False)
        tipo_papel.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('administrador:list_tipo_papel')

@permission_required(perm='administrador', login_url='/webapp/login')
def tipo_papel_listar(request):
    template_name = 'config/tab_base.html'
    context = {}
    context['titulo'] = 'Tipo de papel'
    context['btn_nuevo'] = 'Agregar un tipo de papel'
    context['url_nuevo'] = reverse('administrador:nuevo_tipo_papel')
    context['encabezados'] = [['Nombre', True],
                              ['Editar', False],
                              ['Estatus', True]]
    context['url_ajax'] = reverse('administrador:tab_list_tipo_papel')
    context['url_update_estatus'] = '/administrador/tipo_papel/cambiar_estatus/'
    return render(request, template_name, context)

class TipoPapelAjaxListView(PermissionRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/webapp/login'
    permission_required = 'administrador'
    model = TipoPapel
    columns = [
        'nombre', 'editar', 'estatus'
    ]

    order_columns = [
    'nombre', '', 'estatus'
    ]

    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('administrador:edit_tipo_papel',
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

        return super(TipoPapelAjaxListView, self).render_column(row, column)

    def get_initial_queryset(self):
        return TipoPapel.objects.all()


class TipoPapelActualizar(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/webapp/login'
    permission_required = 'administrador'
    model = TipoPapel
    template_name = 'config/form_1col.html'
    form_class = TipoPapelForm

    def get_context_data(self, **kwargs):
        context = super(TipoPapelActualizar, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Modificación de tipo de papel'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Modifica los campos que requieras'
        return context

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('administrador:list_tipo_papel')

@permission_required(perm='administrador', login_url='/webapp/login')
def tipo_papel_cambiar_estatus(request, pk):
    tipo_papel = get_object_or_404(TipoPapel, pk=pk)
    if tipo_papel.estatus:
        tipo_papel.estatus = False
    else:
        tipo_papel.estatus = True
    tipo_papel.save()
    return JsonResponse({'result': 0})

# Clase PapelImpresion
class PapelImpresionCrear(PermissionRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/webapp/login'
    permission_required = 'administrador'
    model = PapelImpresion
    form_class = PapelImpresionForm
    template_name = 'config/form_1col.html'
    success_url = '/administrador/papel_impresion/listar'

    def get_context_data(self, **kwargs):
        context = super(PapelImpresionCrear, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Registro de papel de impresión'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Completa todos los campos para registrar un papel de impresión'
        return context

    def form_valid(self, form):
        tipoPapel = form.save(commit=False)
        tipoPapel.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('administrador:list_papel_impresion')

@permission_required(perm='administrador', login_url='/webapp/login')
def papel_impresion_listar(request):
    template_name = 'config/tab_base.html'
    context = {}
    context['titulo'] = 'Papel de impresión'
    context['btn_nuevo'] = 'Agregar papel'
    context['url_nuevo'] = reverse('administrador:nuevo_papel_impresion')
    context['encabezados'] = [['Tipo de papel', True],
                              ['Tamaño', True],
                              ['Precio', True],
                              ['Editar', False],
                              ['Estatus', True]]
    context['url_ajax'] = reverse('administrador:tab_list_papel_impresion')
    context['url_update_estatus'] = '/administrador/papel_impresion/cambiar_estatus/'


    return render(request, template_name, context)

class PapelImpresionAjaxListView(PermissionRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/webapp/login'
    permission_required = 'administrador'
    model = PapelImpresion
    columns = [
        'tipo_papel.nombre', 'tamanio.nombre', 'precio',  'editar', 'estatus'
    ]

    order_columns = [
        'tipo_papel.nombre', 'tamanio.nombre', 'precio',  '', 'estatus'
    ]

    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('administrador:edit_papel_impresion',
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

        elif column == 'precio':
            return "${0:,.2f}".format(row.precio)


        return super(PapelImpresionAjaxListView, self).render_column(row, column)

    def get_initial_queryset(self):
        return PapelImpresion.objects.all()

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(tipo_papel__nombre__icontains=search) | qs.filter(precio__icontains=search)| qs.filter(
                tamanio__nombre__icontains=search)
        return qs

class PapelImpresionActualizar(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/webapp/login'
    permission_required = 'administrador'
    model = PapelImpresion
    template_name = 'config/form_1col.html'
    form_class = PapelImpresionForm

    def get_context_data(self, **kwargs):
        context = super(PapelImpresionActualizar, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Modificación del papel de impresión'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Modifica los campos que requieras'
        return context

    def form_valid(self, form):
        # form.instance.set_password(form.cleaned_data['password'])
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('administrador:list_papel_impresion')

@permission_required(perm='administrador', login_url='/webapp/login')
def papel_impresion_cambiar_estatus(request, pk):
    papel_impresion = get_object_or_404(PapelImpresion, pk=pk)
    if papel_impresion.estatus:
        papel_impresion.estatus = False
    else:
        papel_impresion.estatus = True
    papel_impresion.save()
    return JsonResponse({'result': 0})

# Clase Textura
class TexturaCrear(PermissionRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/webapp/login'
    permission_required = 'administrador'
    model = Textura
    form_class = TexturaForm
    template_name = 'config/form_1col.html'
    success_url = '/administrador/textura/listar'

    def get_context_data(self, **kwargs):
        context = super(TexturaCrear, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Registro de textura'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Completa todos los campos para registrar una textura'
        return context

    def form_valid(self, form):
        textura = form.save(commit=False)
        textura.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('administrador:list_textura')

@permission_required(perm='administrador', login_url='/webapp/login')
def textura_listar(request):
    template_name = 'config/tab_base.html'
    context = {}
    context['titulo'] = 'Textura'
    context['btn_nuevo'] = 'Agregar textura'
    context['url_nuevo'] = reverse('administrador:nuevo_textura')
    context['encabezados'] = [['Nombre', True],
                              ['Textura', True],
                              ['Editar', False],
                              ['Estatus', True]]
    context['url_ajax'] = reverse('administrador:tab_list_textura')
    context['url_update_estatus'] = '/administrador/textura/cambiar_estatus/'


    return render(request, template_name, context)
class TexturaAjaxListView(PermissionRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/webapp/login'
    permission_required = 'administrador'
    model = Textura
    columns = [
        'nombre', 'imagen', 'editar', 'estatus'
    ]

    order_columns = [
        'nombre', 'imagen', '', ''
    ]

    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('administrador:edit_textura',
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
                    return '<img style="width:80%" src="'+ row.imagen.url +'" />'


        return super(TexturaAjaxListView, self).render_column(row, column)

    def get_initial_queryset(self):
        return Textura.objects.all()


class TexturaActualizar(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/webapp/login'
    permission_required = 'administrador'
    model = Textura
    template_name = 'config/form_1col.html'
    form_class = TexturaForm

    def get_context_data(self, **kwargs):
        context = super(TexturaActualizar, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Modificación de textura'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Modifica los campos que requieras'
        return context

    def form_valid(self, form):
        # form.instance.set_password(form.cleaned_data['password'])
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('administrador:list_textura')

@permission_required(perm='administrador', login_url='/webapp/login')
def textura_cambiar_estatus(request, pk):
    textura = get_object_or_404(Textura, pk=pk)
    if textura.estatus:
        textura.estatus = False
    else:
        textura.estatus = True
    textura.save()
    return JsonResponse({'result': 0})


# Clase Logo
class LogoCrear(PermissionRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/webapp/login'
    permission_required = 'administrador'
    model = Logo
    form_class = LogoForm
    template_name = 'config/form_1col.html'
    success_url = '/administrador/logo/listar'

    def get_context_data(self, **kwargs):
        context = super(LogoCrear, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Registro de logo'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Completa todos los campos para registrar un logo'
        return context

    def form_valid(self, form):
        logo = form.save(commit=False)
        logo.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('administrador:list_logo')

@permission_required(perm='administrador', login_url='/webapp/login')
def logo_listar(request):
    template_name = 'config/tab_base.html'
    context = {}
    context['titulo'] = 'Logo'
    context['btn_nuevo'] = 'Agregar logo'
    context['url_nuevo'] = reverse('administrador:nuevo_logo')
    context['encabezados'] = [['Nombre', True],
                              ['Logo', True],
                              ['Editar', False],
                              ['Estatus', True]]
    context['url_ajax'] = reverse('administrador:tab_list_logo')
    context['url_update_estatus'] = '/administrador/logo/cambiar_estatus/'

    return render(request, template_name, context)

class LogoAjaxListView(PermissionRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/webapp/login'
    permission_required = 'administrador'
    model = Logo
    columns = [
        'nombre', 'imagen', 'editar', 'estatus'
    ]

    order_columns = [
        'nombre', 'imagen', '', ''
    ]

    max_display_length = 100

    def render_column(self, row, column):
        if column == 'editar':
            return '<a class="" href ="' + reverse('administrador:edit_logo',
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


        return super(LogoAjaxListView, self).render_column(row, column)

    def get_initial_queryset(self):
        return Logo.objects.all()


class LogoActualizar(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/webapp/login'
    permission_required = 'administrador'
    model = Logo
    template_name = 'config/form_1col.html'
    form_class = LogoForm

    def get_context_data(self, **kwargs):
        context = super(LogoActualizar, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Modificación de logo'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Modifica los campos que requieras'
        return context

    def form_valid(self, form):
        # form.instance.set_password(form.cleaned_data['password'])
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('administrador:list_logo')

@permission_required(perm='administrador', login_url='/webapp/login')
def logo_cambiar_estatus(request, pk):
    logo = get_object_or_404(Logo, pk=pk)
    if logo.estatus:
        logo.estatus = False
    else:
        logo.estatus = True
    logo.save()
    return JsonResponse({'result': 0})

# Clase MenuFotopartner
class MenuFotopartnerCrear(PermissionRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/webapp/login'
    permission_required = 'administrador'
    model = MenuFotopartner
    form_class = MenuFotopartnerForm
    template_name = 'config/form_1col.html'
    success_url = '/administrador/MenuFotopartner/listar'

    def get_context_data(self, **kwargs):
        context = super(MenuFotopartnerCrear, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Registro de Menu Foto partner'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Completa todos los campos para registrar un menu'
        return context

    def form_valid(self, form):
        menu = form.save(commit=False)
        menu.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('administrador:list_MenuFotopartner')

@permission_required(perm='administrador', login_url='/webapp/login')
def MenuFotopartner_listar(request):
    template_name = 'config/tab_base.html'
    context = {}
    context['titulo'] = 'MenuFotopartner'
    context['btn_nuevo'] = 'Agregar MenuFotopartner'
    context['url_nuevo'] = reverse('administrador:nuevo_MenuFotopartner')
    context['encabezados'] = [['Nombre', True],
                              ['Editar', False],
                              ['Estatus', True]]
    context['url_ajax'] = reverse('administrador:tab_list_MenuFotopartner')
    context['url_update_estatus'] = '/administrador/MenuFotopartner/cambiar_estatus/'

    return render(request, template_name, context)

class MenuFotopartnerAjaxListView(PermissionRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/webapp/login'
    permission_required = 'administrador'
    model = MenuFotopartner
    columns = [
        'nombre', 'editar', 'estatus'
    ]

    order_columns = [
        'nombre', '', ''
    ]

    max_display_length = 100

    def render_column(self, row, column):
        if column == 'editar':
            return '<a class="" href ="' + reverse('administrador:edit_MenuFotopartner',
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
                    return '<img style="width:80%" src="'+ row.imagen.url +'" />'


        return super(MenuFotopartnerAjaxListView, self).render_column(row, column)

    def get_initial_queryset(self):
        return MenuFotopartner.objects.all()

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(nombre__icontains=search)
        return qs


class MenuFotopartnerActualizar(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/webapp/login'
    permission_required = 'administrador'
    model = MenuFotopartner
    template_name = 'config/form_1col.html'
    form_class = MenuFotopartnerForm

    def get_context_data(self, **kwargs):
        context = super(MenuFotopartnerActualizar, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Modificación de menu fotopartner'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Modifica los campos que requieras'
        return context

    def form_valid(self, form):
        # form.instance.set_password(form.cleaned_data['password'])
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('administrador:list_MenuFotopartner')


@permission_required(perm='administrador', login_url='/webapp/login')
def MenuFotopartner_cambiar_estatus(request, pk):
    menu_fotopartner = get_object_or_404(MenuFotopartner, pk=pk)
    if menu_fotopartner.estatus:
        menu_fotopartner.estatus = False
    else:
        menu_fotopartner.estatus = True
    menu_fotopartner.save()
    return JsonResponse({'result': 0})

# Clase Promocion
class PromocionCrear(PermissionRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/webapp/login'
    permission_required = 'administrador'
    model = Promocion
    form_class = PromocionForm
    template_name = 'config/form_1col.html'
    success_url = '/administrador/Promocion/listar'

    def get_context_data(self, **kwargs):
        context = super(PromocionCrear, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Registro de promoción'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Completa todos los campos para registrar una promocion'
        return context

    def form_valid(self, form):
        menu = form.save(commit=False)
        menu.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('administrador:list_Promocion')

@permission_required(perm='administrador', login_url='/webapp/login')
def Promocion_listar(request):
    template_name = 'config/tab_base.html'
    context = {}
    context['titulo'] = 'Promoción'
    context['btn_nuevo'] = 'Agregar Promoción'
    context['url_nuevo'] = reverse('administrador:nuevo_Promocion')
    context['encabezados'] = [['Código de promoción', True],
                              ['Editar', False],
                              ['Estatus', True]]
    context['url_ajax'] = reverse('administrador:tab_list_Promocion')
    context['url_update_estatus'] = '/administrador/Promocion/cambiar_estatus/'

    return render(request, template_name, context)

class PromocionAjaxListView(PermissionRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/webapp/login'
    permission_required = 'administrador'
    model = Promocion
    columns = [
        'nombre', 'editar', 'estatus'
    ]

    order_columns = [
        'nombre', '', ''
    ]

    max_display_length = 100

    def render_column(self, row, column):
        if column == 'editar':
            return '<a class="" href ="' + reverse('administrador:edit_Promocion',
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
                    return '<img style="width:80%" src="'+ row.imagen.url +'" />'


        return super(PromocionAjaxListView, self).render_column(row, column)

    def get_initial_queryset(self):
        return Promocion.objects.all()

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(url__icontains=search)
        return qs


class PromocionActualizar(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/webapp/login'
    permission_required = 'administrador'
    model = Promocion
    template_name = 'config/form_1col.html'
    form_class = PromocionForm

    def get_context_data(self, **kwargs):
        context = super(PromocionActualizar, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Modificación de promoción'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Modifica los campos que requieras'
        return context

    def form_valid(self, form):
        # form.instance.set_password(form.cleaned_data['password'])
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('administrador:list_Promocion')

@permission_required(perm='administrador', login_url='/webapp/login')
def Promocion_cambiar_estatus(request, pk):
    promo = get_object_or_404(Promocion, pk=pk)
    if promo.estatus:
        promo.estatus = False
    else:
        promo.estatus = True
    promo.save()
    return JsonResponse({'result': 0})

# Clase Categoria
class CategoriaCrear(PermissionRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/webapp/login'
    permission_required = 'administrador'
    model = Categoria
    form_class = CategoriaForm
    template_name = 'config/form_1col.html'
    success_url = '/administrador/categoria/listar'

    def get_context_data(self, **kwargs):
        context = super(CategoriaCrear, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Registro de categoría'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Completa todos los campos para registrar una categoria'
        return context

    def form_valid(self, form):
        menu = form.save(commit=False)
        menu.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('administrador:list_categoria')

@permission_required(perm='administrador', login_url='/webapp/login')
def Categoria_listar(request):
    template_name = 'config/tab_base.html'
    context = {}
    context['titulo'] = 'Categoría'
    context['btn_nuevo'] = 'Agregar categoría'
    context['url_nuevo'] = reverse('administrador:nuevo_categoria')
    context['encabezados'] = [['Nombre', True],
                              ['Editar', False],
                              ['Estatus', True]]
    context['url_ajax'] = reverse('administrador:tab_list_categoria')
    context['url_update_estatus'] = '/administrador/categoria/cambiar_estatus/'

    return render(request, template_name, context)

class CategoriaAjaxListView(PermissionRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/webapp/login'
    permission_required = 'administrador'
    model = Promocion
    columns = [
        'nombre', 'editar', 'estatus'
    ]

    order_columns = [
        'nombre', '', ''
    ]

    max_display_length = 100

    def render_column(self, row, column):
        if column == 'editar':
            return '<a class="" href ="' + reverse('administrador:edit_categoria',
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
                    return '<img style="width:80%" src="'+ row.imagen.url +'" />'


        return super(CategoriaAjaxListView, self).render_column(row, column)

    def get_initial_queryset(self):
        return Categoria.objects.all()

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(nombre__icontains=search)
        return qs


class CategoriaActualizar(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/webapp/login'
    permission_required = 'administrador'
    model = Categoria
    template_name = 'config/form_1col.html'
    form_class = CategoriaForm

    def get_context_data(self, **kwargs):
        context = super(CategoriaActualizar, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Modificación de categoría'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Modifica los campos que requieras'
        return context

    def form_valid(self, form):
        # form.instance.set_password(form.cleaned_data['password'])
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('administrador:list_Promocion')

@permission_required(perm='administrador', login_url='/webapp/login')
def Categoria_cambiar_estatus(request, pk):
    promo = get_object_or_404(Categoria, pk=pk)
    if promo.estatus:
        promo.estatus = False
    else:
        promo.estatus = True
    promo.save()
    return JsonResponse({'result': 0})

# Personal Administrativo
class PersonalAdministrativoCrear(PermissionRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/webapp/login'
    permission_required = 'add_personaladministrativo'
    model = PersonalAdministrativo
    form_class = PersonalAdministrativoForm
    template_name = 'config/form_1col.html'

    def get_context_data(self, **kwargs):
        context = super(PersonalAdministrativoCrear, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Registro de Personal'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Completa todos los campos para registrar un personal'
        return context

    def form_valid(self, form):
        rol = Rol.objects.get(pk=5)
        personal = form.save(commit=False)
        personal.set_password(personal.password)
        personal.rol = rol
        personal.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('administrador:list_personal_administrativo')

@permission_required(perm='add_personaladministrativo', login_url='/webapp/login')
def personal_administrativo_listar(request):
    template_name = 'config/tab_base.html'
    context = {}
    context['titulo'] = 'Personal'
    context['btn_nuevo'] = 'Agregar personal'
    context['url_nuevo'] = reverse('administrador:nuevo_personal_administrativo')
    context['encabezados'] = [['Nombre', True],
                              ['Correo', True],
                              ['Editar', False],
                              ['Estatus', True]]
    context['url_ajax'] = reverse('administrador:tab_list_personal_administrativo')
    context['url_update_estatus'] = '/administrador/personal_administrativo/cambiar_estatus/'
    return render(request, template_name, context)

class PersonalAdministrativoAjaxListView(PermissionRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/webapp/login'
    permission_required = 'add_personaladministrativo'
    model = PersonalAdministrativo
    columns = ['nombre','correo', 'editar', 'estatus']

    order_columns = ['nombre', 'correo', '', 'estatus']

    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('administrador:edit_personal_administrativo',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><i class="far fa-edit"></i></a>'

        elif column == 'estatus':
            if row.estatus:
                return '<div class="custom-control custom-switch"><input type="checkbox" checked class="custom-control-input" onchange=cambiar_estatus(' + str(
                    row.pk) + ') id="customSwitch'+str(row.pk)+'"><label class="custom-control-label" for="customSwitch'+str(row.pk)+'">On</label></div>'
            else:
                return '<div class="custom-control custom-switch"><input type="checkbox" class="custom-control-input" onchange=cambiar_estatus(' + str(
                    row.pk) + ') id="customSwitch'+str(row.pk)+'"><label class="custom-control-label" for="customSwitch'+str(row.pk)+'">Off</label></div>'

        return super(PersonalAdministrativoAjaxListView, self).render_column(row, column)

    def get_initial_queryset(self):
        return PersonalAdministrativo.objects.all()

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(nombre__icontains=search) | qs.filter(id__icontains=search) | qs.filter(correo__icontains=search)
        return qs


class PersonalAdministrativoActualizar(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/webapp/login'
    permission_required = 'add_personaladministrativo'
    model = PersonalAdministrativo
    template_name = 'config/form_1col.html'
    form_class = PersonalAdministrativoForm

    def get_context_data(self, **kwargs):
        context = super(PersonalAdministrativoActualizar, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Modificación de personal'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Modifica los campos que requieras'
        return context

    def form_valid(self, form):
        form.instance.set_password(form.cleaned_data['password'])
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('administrador:list_personal_administrativo')

@permission_required(perm='add_personaladministrativo', login_url='/webapp/login')
def personal_administrativo_cambiar_estatus(request, pk):
    personal = get_object_or_404(PersonalAdministrativo, pk=pk)
    if personal.estatus:
        personal.estatus = False
    else:
        personal.estatus = True
    personal.save()
    return JsonResponse({'result': 0})

@permission_required(perm='administrador', login_url='/webapp/login')
def ventas_listar(request):
    template_name = 'config/tab_base.html'
    context = {}
    context['titulo'] = 'Ventas'
    context['encabezados'] = [['ID', True],
                              ['Fecha de compra', True],
                              ['Usuario', True],
                              ['Dirección', True],
                              ['Método de pago', True],
                              ['Detalle de pago', True],
                              ['Total', True],
                              ['Estatus', True],
                              ['Detalle', False],
                              ]
    context['url_ajax'] = reverse('administrador:tab_list_ventas')
    return render(request, template_name, context)

class VentasAjaxListView(PermissionRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/webapp/login'
    permission_required = 'administrador'
    model = Orden
    columns = ['id','fecha_compra', 'usuario.nombre', 'direccion', 'forma_pago.nombre', 'detalle_pago', 'total', 'estatus.nombre', 'detalle']

    order_columns = ['id', 'fecha_compra', 'usuario.nombre', 'colonia', 'forma_pago.nombre', '', 'total', 'estatus.nombre', '']

    max_display_length = 100
    settingstime_zone = timezone(settings.TIME_ZONE)
    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('administrador:edit_personal_administrativo',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><i class="material-icons">edit</i></a>'

        elif column == 'estatus':
            return '<a class="" href ="#"><i class="material-icons">receipt</i></a>'
        elif column == 'estatus':
            return '<a class="" href ="#"><i class="material-icons">receipt</i></a>'
        elif column == 'fecha_compra':
            if row.fecha_compra:
                return row.fecha_compra.astimezone(self.settingstime_zone).strftime("%d-%b-%Y %H:%M")
            return 'Sin Fecha'
        elif column == 'direccion':
            if row.direccion:
                return row.direccion.direccion_completa()
            return 'Sin definir'
        elif column == 'total':
            return "$" + "{0:,.2f}".format(row.total)
        elif column == 'detalle_pago':
            if row.forma_pago.nombre == 'Tarjeta':
                return '**** **** **** ' + row.tarjeta.ultimos_digitos
            elif row.forma_pago.nombre == 'Oxxo':
                return row.oxxo_order
            elif row.forma_pago.nombre == 'Spei':
                return 'Transferencia'
            return 'Sin información'
        elif column == 'detalle':
            return '<a class="" href ="' + reverse('administrador:detalle_orden',
                                                   kwargs={
                                                       'orden': row.pk}) + '"><i class="fa fa-file-invoice" aria-hidden="true"></i></a>'
        return super(VentasAjaxListView, self).render_column(row, column)

    def get_initial_queryset(self):
        return Orden.objects.filter(estatus__nombre="Pagado", estatus_compra__nombre="Ordenado")

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(usuario__nombre__icontains=search) | qs.filter(id__icontains=search) | qs.filter(
                forma_pago__nombre__icontains=search)| qs.filter(forma_pago__nombre__icontains=search)
        return qs

@permission_required(perm='administrador', login_url='/webapp/login')
def detalle_orden(request, orden):
    template_name = 'administrador/detalle_orden.html'
    orden_objt = Orden.objects.get(pk=orden, estatus_compra__nombre='Ordenado')
    productos = Producto.objects.filter(orden=orden_objt)
    if request.method == 'POST':
        est_compra = EstatusCompra.objects.get(pk=3)
        num_guia = request.POST['num_guia']
        orden_objt.num_guia=num_guia
        orden_objt.estatus_compra = est_compra # Impresion y envío
        orden_objt.save()
        return HttpResponseRedirect(reverse('administrador:list_ventas'))
    return render(request, template_name, context={'orden':orden_objt, 'productos': productos})

@permission_required(perm='administrador', login_url='/webapp/login')
def producto_descarga(request, token, image_name):
    context = {}
    template_error = 'cliente/error_descarga.html'
    try:
        decode_descarga = jwt.decode(token, KEY_FOTO, algorithm='HS256')
        producto = Producto.objects.get(pk=decode_descarga['producto'])
        foto = Fotografia.objects.get(pk=producto.foto.pk)
        with open('/var/django'+foto.foto_original.url, "rb") as f:
            return HttpResponse(f.read(), content_type="image/jpeg")
    except:
        context['error'] = 'El link no es válido'
    return render(request, template_error, context)

@permission_required(perm='administrador', login_url='/webapp/login')
def historial_ventas_listar(request):
    template_name = 'config/tab_base.html'
    context = {}
    context['titulo'] = 'Historial de ventas'
    context['encabezados'] = [['ID', True],
                              ['Fecha de solicitud', True],
                              ['Fecha de compra', True],
                              ['Usuario', True],
                              ['Dirección', True],
                              ['Método de pago', True],
                              ['Detalle de pago', True],
                              ['Total', True],
                              ['Estatus', True],
                              ['Detalle', False],
                              ]
    context['url_ajax'] = reverse('administrador:tab_list_historial_ventas')
    return render(request, template_name, context)

class HistorialVentasAjaxListView(PermissionRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/webapp/login'
    permission_required = 'administrador'
    model = Orden
    columns = ['id','fecha_creacion', 'fecha_compra', 'usuario.nombre', 'direccion', 'forma_pago.nombre', 'detalle_pago', 'total', 'estatus.nombre', 'detalle']

    order_columns = ['id', 'fecha_creacion', 'fecha_compra', 'usuario.nombre', 'colonia', 'forma_pago.nombre', '', 'total', 'estatus.nombre', '']

    max_display_length = 100
    settingstime_zone = timezone(settings.TIME_ZONE)
    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('administrador:edit_personal_administrativo',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><i class="material-icons">edit</i></a>'

        elif column == 'estatus':
            return '<a class="" href ="#"><i class="material-icons">receipt</i></a>'
        elif column == 'estatus':
            return '<a class="" href ="#"><i class="material-icons">receipt</i></a>'
        elif column == 'fecha_compra':
            if row.fecha_compra:
                return row.fecha_compra.astimezone(self.settingstime_zone).strftime("%d-%b-%Y %H:%M")
            return 'Sin fecha'
        elif column == 'direccion':
            if row.direccion:
                return row.direccion.direccion_completa()
            return 'Sin definir'
        elif column == 'total':
            return "$" + "{0:,.2f}".format(row.total)
        elif column == 'detalle_pago':
            if row.forma_pago.nombre=='Tarjeta':
                return '**** **** **** '+row.tarjeta.ultimos_digitos
            elif row.forma_pago.nombre=='Oxxo':
                return row.oxxo_order
            elif row.forma_pago.nombre=='Spei':
                return 'Transferencia'
            return 'Sin información'
        return super(HistorialVentasAjaxListView, self).render_column(row, column)

    def get_initial_queryset(self):
        return Orden.objects.filter(estatus__pk__in=[1,2])

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(usuario__nombre__icontains=search) | qs.filter(id__icontains=search) | qs.filter(
                forma_pago__nombre__icontains=search)| qs.filter(forma_pago__nombre__icontains=search)
        return qs

@permission_required(perm='administrador', login_url='/webapp/login')
def fotografo_cambiar_estatus(request, pk):
    personal = get_object_or_404(Fotografo, pk=pk)
    if personal.estatus:
        personal.estatus = False
    else:
        personal.estatus = True
    personal.save()
    return JsonResponse({'result': 0})

@permission_required(perm='administrador', login_url='/webapp/login')
def fotografo_cambiar_confiable(request, pk):
    fotografo = get_object_or_404(Fotografo, pk=pk)
    if fotografo.confiable:
        fotografo.confiable = False
    else:
        fotografo.confiable = True
    fotografo.save()
    return JsonResponse({'result': 0})

@permission_required(perm='administrador', login_url='/webapp/login')
def usuarios_generales_listar(request):
    template_name = 'config/tab_base.html'
    context = {}
    context['titulo'] = 'Usuarios generales'
    context['encabezados'] = [['ID', True],
                              ['Nombre', True],
                              ['Correo', True],
                              ['Estatus', True],
                              ['Detalle', False],
                              ]
    context['url_ajax'] = reverse('administrador:tab_list_usuarios_generales')
    context['url_update_estatus'] = '/administrador/fotografo/cambiar_estatus/'
    return render(request, template_name, context)

class UsuariosGeneralesAjaxListView(PermissionRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/webapp/login'
    permission_required = 'administrador'
    model = Orden
    columns = ['id', 'nombre', 'correo', 'estatus', 'detalle']

    order_columns = ['id', 'nombre', 'correo', 'estatus', '']

    max_display_length = 100
    settingstime_zone = timezone(settings.TIME_ZONE)
    def render_column(self, row, column):

        if column == 'detalle':
            return '<a class="" href ="'+reverse('administrador:detalle_usuario', kwargs={'pk': row.pk})+'"><i class="fa fa-users"></i></a>'
        elif column == 'estatus':
            if row.estatus:
                return '<div class="custom-control custom-switch"><input type="checkbox" checked class="custom-control-input" onchange=cambiar_estatus(' + str(
                    row.pk) + ') id="customSwitch'+str(row.pk)+'"><label class="custom-control-label" for="customSwitch'+str(row.pk)+'">On</label></div>'
            else:
                return '<div class="custom-control custom-switch"><input type="checkbox" class="custom-control-input" onchange=cambiar_estatus(' + str(
                    row.pk) + ') id="customSwitch'+str(row.pk)+'"><label class="custom-control-label" for="customSwitch'+str(row.pk)+'">Off</label></div>'

        return super(UsuariosGeneralesAjaxListView, self).render_column(row, column)

    def get_initial_queryset(self):
        return Fotografo.objects.filter(fotopartner=False)

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(nombre__icontains=search) | qs.filter(id__icontains=search) | qs.filter(
                correo__icontains=search)| qs.filter(estatus__icontains=search)
        return qs


@permission_required(perm='administrador', login_url='/webapp/login')
def fotopartners_listar(request):
    template_name = 'config/tab_base.html'
    context = {}
    context['titulo'] = 'Usuarios Fotopartners'
    context['encabezados'] = [['ID', True],
                              ['Nombre', True],
                              ['Correo', True],
                              ['Confiable', True],
                              ['Estatus', True],
                              ['Detalle', False],
                              ]
    context['url_ajax'] = reverse('administrador:tab_list_fotopartners')
    context['url_update_estatus'] = '/administrador/fotografo/cambiar_estatus/'
    context['url_update_confiable'] = '/administrador/fotografo/cambiar_confiable/'
    context['script_extra'] = '/static/js/tab_utils.js'
    return render(request, template_name, context)

class FotopartnersAjaxListView(PermissionRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/webapp/login'
    permission_required = 'administrador'
    model = Orden
    columns = ['id', 'nombre', 'correo', 'confiable', 'estatus', 'detalle']

    order_columns = ['id', 'nombre', 'correo', 'confiable', 'estatus', '']

    max_display_length = 100
    settingstime_zone = timezone(settings.TIME_ZONE)
    def render_column(self, row, column):

        if column == 'detalle':
            return '<a class="" href ="'+reverse('administrador:detalle_usuario', kwargs={'pk': row.pk})+'"><i class="fa fa-users"></i></a>'
        elif column == 'estatus':
            if row.estatus:
                return '<div class="custom-control custom-switch"><input type="checkbox" checked class="custom-control-input" onchange=cambiar_estatus(' + str(
                    row.pk) + ') id="customSwitch'+str(row.pk)+'"><label class="custom-control-label" for="customSwitch'+str(row.pk)+'">On</label></div>'
            else:
                return '<div class="custom-control custom-switch"><input type="checkbox" class="custom-control-input" onchange=cambiar_estatus(' + str(
                    row.pk) + ') id="customSwitch'+str(row.pk)+'"><label class="custom-control-label" for="customSwitch'+str(row.pk)+'">Off</label></div>'
        elif column == 'confiable':
            if row.confiable:
                return '<div class="custom-control custom-switch"><input type="checkbox" checked class="custom-control-input" onchange=cambiar_confiable(' + str(
                    row.pk) + ') id="switchConfiable' + str(
                    row.pk) + '"><label class="custom-control-label" for="switchConfiable' + str(
                    row.pk) + '">On</label></div>'
            else:
                return '<div class="custom-control custom-switch"><input type="checkbox" class="custom-control-input" onchange=cambiar_confiable(' + str(
                    row.pk) + ') id="switchConfiable' + str(
                    row.pk) + '"><label class="custom-control-label" for="switchConfiable' + str(
                    row.pk) + '">Off</label></div>'

        return super(FotopartnersAjaxListView, self).render_column(row, column)

    def get_initial_queryset(self):
        return Fotografo.objects.filter(fotopartner=True)

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(nombre__icontains=search) | qs.filter(id__icontains=search) | qs.filter(
                correo__icontains=search)| qs.filter(estatus__icontains=search)| qs.filter(confiable__icontains=search)
        return qs

@permission_required(perm='administrador', login_url='/webapp/login')
def usuarios_bloqueados_listar(request):
    template_name = 'config/tab_base.html'
    context = {}
    context['titulo'] = 'Usuarios bloqueados'
    context['encabezados'] = [['ID', True],
                              ['Nombre', True],
                              ['Correo', True],
                              ['Estatus', True],
                              ['Detalle', False],
                              ]
    context['url_ajax'] = reverse('administrador:tab_list_usuarios_bloqueados')
    context['url_update_estatus'] = '/administrador/fotografo/cambiar_estatus/'
    return render(request, template_name, context)

class UsuariosBloqueadosAjaxListView(PermissionRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/webapp/login'
    permission_required = 'administrador'
    model = Orden
    columns = ['id', 'nombre', 'correo', 'estatus', 'detalle']

    order_columns = ['id', 'nombre', 'correo', 'estatus', '']

    max_display_length = 100
    settingstime_zone = timezone(settings.TIME_ZONE)
    def render_column(self, row, column):

        if column == 'detalle':
            return '<a class="" href ="'+reverse('administrador:detalle_usuario', kwargs={'pk': row.pk})+'"><i class="fa fa-users"></i></a>'
        elif column == 'estatus':
            if row.estatus:
                return '<div class="custom-control custom-switch"><input type="checkbox" checked class="custom-control-input" onchange=cambiar_estatus(' + str(
                    row.pk) + ') id="customSwitch'+str(row.pk)+'"><label class="custom-control-label" for="customSwitch'+str(row.pk)+'">On</label></div>'
            else:
                return '<div class="custom-control custom-switch"><input type="checkbox" class="custom-control-input" onchange=cambiar_estatus(' + str(
                    row.pk) + ') id="customSwitch'+str(row.pk)+'"><label class="custom-control-label" for="customSwitch'+str(row.pk)+'">Off</label></div>'

        return super(UsuariosBloqueadosAjaxListView, self).render_column(row, column)

    def get_initial_queryset(self):
        return Fotografo.objects.filter(estatus=False)

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(nombre__icontains=search) | qs.filter(id__icontains=search) | qs.filter(
                correo__icontains=search)| qs.filter(estatus__icontains=search)
        return qs

@permission_required(perm='administrador', login_url='/webapp/login')
def aprobar_foto_listar(request):
    template_name = 'config/tab_aprobar_foto.html'
    context = {}
    context['titulo'] = 'Aprobar fotografías'
    context['encabezados'] = [['ID', True],
                              ['Fecha de publicación', True],
                              ['Usuario', True],
                              ['Nombre de la imagen', True],
                              ['Tamaño', True],
                              ['Tipo de fotografía', True],
                              ['Descripción técnica', True],
                              ['Aprobar', False],
                              ['Foto', False],
                              ]
    context['url_ajax'] = reverse('administrador:tab_list_aprobar_foto')
    context['url_update_estatus'] = '/administrador/foto/cambiar_estatus/'
    context['url_update_rechazar'] = '/administrador/foto/rechazar/'
    return render(request, template_name, context)

class AprobarFotoAjaxListView(PermissionRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/webapp/login'
    permission_required = 'administrador'
    model = Fotografia
    columns = ['id', 'fecha_alta', 'usuario.nombre', 'nombre', 'tamanio.nombre', 'tipo_foto.nombre', 'descripcion', 'aprobar', 'foto']

    order_columns = ['id', 'fecha_alta', 'usuario.nombre', 'nombre', 'tamanio.nombre', 'tipo_foto.nombre', 'descripcion', '', '']

    max_display_length = 100
    settingstime_zone = timezone(settings.TIME_ZONE)
    def render_column(self, row, column):

        if column == 'foto':
            return '<img style="width:100%" src="' + row.foto_original.url + '" />'
        elif column == 'aprobar':
            return '<div  class="buttons-copy buttons-html5" tabindex="0" aria-controls="tabla" onclick=cambiar_estatus('+ str(
                row.pk) +')><a class="btn generalBtn"><i class="fa fa-check" aria-hidden="true"></i> Aprobar</a></div>' \
                         '<div  class="buttons-copy buttons-html5" tabindex="0" aria-controls="tabla" onclick=rechazar('+ str(
                row.pk) +')><a class="btn generalBtn" style="background: #dc3545 !important"><i class="fa fa-times-circle" aria-hidden="true"></i> Rechazar</a></div>'
        return super(AprobarFotoAjaxListView, self).render_column(row, column)

    def get_initial_queryset(self):
        return Fotografia.objects.filter(aprobada=False, estatus=True)

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(nombre__icontains=search) | qs.filter(id__icontains=search) | qs.filter(
                correo__icontains=search)| qs.filter(estatus__icontains=search)
        return qs

@permission_required(perm='administrador', login_url='/webapp/login')
def foto_aprobar(request, pk):
    foto = get_object_or_404(Fotografia, pk=pk)
    foto.aprobada = True
    foto.save()
    return JsonResponse({'result': 0})\

@permission_required(perm='administrador', login_url='/webapp/login')
def foto_rechazar(request, pk):
    foto = get_object_or_404(Fotografia, pk=pk)
    foto.estatus = False
    foto.save()
    return JsonResponse({'result': 0})

@permission_required(perm='administrador', login_url='/webapp/login')
def contactanos_listar(request):
    template_name = 'config/tab_base.html'
    context = {}
    context['titulo'] = 'Datos de contacto'
    context['encabezados'] = [['Dirección', True],
                              ['Correo', True],
                              ['Teléfono', True],
                              ['Editar', False]]
    context['url_ajax'] = reverse('administrador:tab_list_contactanos')
    context['url_update_estatus'] = '/administrador/contactanos/cambiar_estatus/'


    return render(request, template_name, context)

class ContactanosListarAjaxListView(PermissionRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/webapp/login'
    permission_required = 'administrador'
    model = Contactanos
    columns = ['direccion', 'correo', 'telefono', 'editar']
    order_columns = ['direccion', 'correo', 'telefono', '']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('administrador:edit_contactanos',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><i class="far fa-edit"></i></a>'

        return super(ContactanosListarAjaxListView, self).render_column(row, column)

    def get_initial_queryset(self):
        return Contactanos.objects.all()

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(codigo__icontains=search) | qs.filter(id__icontains=search)
        return qs


class ContactanosActualizar(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/webapp/login'
    permission_required = 'administrador'
    model = Contactanos
    template_name = 'config/form_1col.html'
    form_class = ContactanosForm

    def get_context_data(self, **kwargs):
        context = super(ContactanosActualizar, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Modificación de código de marco'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Modifica los campos que requieras'
        return context

    def form_valid(self, form):
        # form.instance.set_password(form.cleaned_data['password'])
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('administrador:list_contactanos')


class DetalleUsuario(PermissionRequiredMixin, DetailView):
    redirect_field_name = 'next'
    login_url = '/webapp/login'
    permission_required = 'administrador'
    model = Fotografo
    template_name = 'administrador/detalle_usuario.html'

    def get_context_data(self, **kwargs):
        context = super(DetalleUsuario, self).get_context_data(**kwargs)
        fotografo = Fotografo.objects.get(pk=self.kwargs['pk'])
        context['usuario'] = fotografo
        return context

@permission_required(perm='administrador', login_url='/webapp/login')
def menu(request):
    template_name = 'administrador/menu.html'
    return render(request, template_name)

@permission_required(perm='administrador', login_url='/webapp/login')
def vista_catalogos(request):
    template_name = 'administrador/catalogos.html'
    return render(request, template_name)

class FotoPrecioCrear(PermissionRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/webapp/login'
    permission_required = 'administrador'
    model = FotoPrecio
    form_class = FotoPrecioForm
    template_name = 'config/form_1col.html'
    success_url = '/administrador/foto_precio/listar'

    def get_context_data(self, **kwargs):
        context = super(FotoPrecioCrear, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Registro de precios de fotos'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Completa todos los campos para registrar un costo de foto por tamaño'
        return context

    def form_valid(self, form):
        tipoPapel = form.save(commit=False)
        tipoPapel.min_area  = tipoPapel.min_altura * tipoPapel.min_ancho
        tipoPapel.max_area  = tipoPapel.max_altura * tipoPapel.max_ancho
        tipoPapel.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('administrador:list_foto_precio')

@permission_required(perm='administrador', login_url='/webapp/login')
def foto_precio_listar(request):
    template_name = 'config/tab_base.html'
    context = {}
    context['titulo'] = 'Precios de fotografías'
    context['btn_nuevo'] = 'Agregar precio'
    context['url_nuevo'] = reverse('administrador:nuevo_foto_precio')
    context['encabezados'] = [['Tipo de foto', True],
                              ['Tamaño', True],
                              ['Rango (Ancho x Alto) Px.', True],
                              ['Precio', True],
                              ['Editar', False],
                              ['Estatus', True]]
    context['url_ajax'] = reverse('administrador:tab_list_foto_precio')
    context['url_update_estatus'] = '/administrador/foto_precio/cambiar_estatus/'


    return render(request, template_name, context)

class FotoPrecioAjaxListView(PermissionRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/webapp/login'
    permission_required = 'administrador'
    model = FotoPrecio
    columns = [
        'tipo_foto.nombre', 'tamanio.nombre', 'rango', 'precio',  'editar', 'estatus'
    ]

    order_columns = [
        'tipo_foto.nombre', 'tamanio.nombre', 'min_area', 'precio',  '', 'estatus'
    ]

    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('administrador:edit_foto_precio',
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
        elif column == 'rango':
            return str(row.min_ancho)+'x'+str(row.min_altura)+' - '+str(row.max_ancho)+'x'+str(row.max_altura)

        elif column == 'precio':
            return "${0:,.2f}".format(row.precio)


        return super(FotoPrecioAjaxListView, self).render_column(row, column)

    def get_initial_queryset(self):
        return FotoPrecio.objects.all()

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(tipo_papel__nombre__icontains=search) | qs.filter(precio__icontains=search)| qs.filter(
                tamanio__nombre__icontains=search)
        return qs

class FotoPrecioActualizar(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/webapp/login'
    permission_required = 'administrador'
    model = FotoPrecio
    template_name = 'config/form_1col.html'
    form_class = FotoPrecioForm

    def get_context_data(self, **kwargs):
        context = super(FotoPrecioActualizar, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Modificación del precio de fotografías'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Modifica los campos que requieras'
        return context

    def form_valid(self, form):
        tipoPapel = form.save(commit=False)
        tipoPapel.min_area = tipoPapel.min_altura * tipoPapel.min_ancho
        tipoPapel.max_area = tipoPapel.max_altura * tipoPapel.max_ancho
        tipoPapel.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('administrador:list_foto_precio')

@permission_required(perm='administrador', login_url='/webapp/login')
def foto_precio_cambiar_estatus(request, pk):
    foto_precio = get_object_or_404(FotoPrecio, pk=pk)
    if foto_precio.estatus:
        foto_precio.estatus = False
    else:
        foto_precio.estatus = True
    foto_precio.save()
    return JsonResponse({'result': 0})


# @permission_required(perm='', login_url='/webapp/login')
def vista_perfil(request):
    template_name = 'cliente/perfil.html'
    return render(request, template_name)