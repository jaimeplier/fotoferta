from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
# Create your views here.
from django.urls import reverse
from django.views.generic import CreateView, UpdateView
from pytz import timezone

from administrador.forms import CodigoMarcoForm, MarcoForm, MarialuisaForm, TamanioForm, ModeloMarialuisaForm, \
    GrosorPapelForm, TipoPapelForm, TexturaForm, LogoForm, PersonalAdministrativoForm, MenuFotopartnerForm, \
    PromocionForm
from config.models import CodigoMarco, Marco, MariaLuisa, ModeloMariaLuisa, Tamanio, GrosorPapel, TipoPapel, Textura, \
    Logo, PersonalAdministrativo, Rol, Orden, MenuFotopartner, Promocion, Fotografo
from django_datatables_view.base_datatable_view import BaseDatatableView

from fotofertas import settings


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
                                                       'pk': row.pk}) + '"><i class="material-icons">edit</i></a>'

        elif column == 'estatus':
            if row.estatus:
                return '<div class="switch"><label>Off<input type="checkbox" checked onchange=cambiar_estatus(' + str(
                    row.pk) + ')><span class="lever"></span>On</label></div>'
            else:
                return '<div class="switch"><label>Off<input type="checkbox" onchange=cambiar_estatus(' + str(
                    row.pk) + ')><span class="lever"></span>On</label></div>'

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
    template_name = 'administrador/tab_tamanio.html'
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
                                                       'pk': row.pk}) + '"><i class="material-icons">edit</i></a>'

        elif column == 'estatus':
            if row.estatus:
                return '<div class="switch"><label>Off<input type="checkbox" checked onchange=cambiar_estatus(' + str(
                    row.pk) + ')><span class="lever"></span>On</label></div>'
            else:
                return '<div class="switch"><label>Off<input type="checkbox" onchange=cambiar_estatus(' + str(
                    row.pk) + ')><span class="lever"></span>On</label></div>'

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
                                                       'pk': row.pk}) + '"><i class="material-icons">edit</i></a>'
        elif column == 'imagen_horizontal':
            if row.imagen_horizontal.url:
                print(row)
                return '<img style="width:100%" src="'+ row.imagen_horizontal.url +'" />'
        elif column == 'imagen_vertical':
            if row.imagen_vertical.url:
                return '<img style="width:100%" src="'+ row.imagen_vertical.url +'" />'

        elif column == 'precio':
            return "${0:,.2f}".format(row.precio)

        elif column == 'estatus':
            if row.estatus:
                return '<div class="switch"><label>Off<input type="checkbox" checked onchange=cambiar_estatus(' + str(
                    row.pk) + ')><span class="lever"></span>On</label></div>'
            else:
                return '<div class="switch"><label>Off<input type="checkbox" onchange=cambiar_estatus(' + str(
                    row.pk) + ')><span class="lever"></span>On</label></div>'

        return super(MarcoListarAjaxListView, self).render_column(row, column)

    def get_initial_queryset(self):
        return Marco.objects.all()
        
    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(nombre__icontains=search) | qs.filter(id__icontains=search) | qs.filter(codigo__icontains=search) | \
                qs.filter(tamanio__icontains=search) | qs.filter(alto__icontains=search) | qs.filter(ancho__icontains=search) | \
                qs.filter(grosor_lado__icontains=search) | qs.filter(grosor_total__icontains=search) | qs.filter(grosor_final__icontains=search) | \
                qs.filter(profundidad__icontains=search) | qs.filter(peso__icontains=search) | qs.filter(precio__icontains=search) | \
                qs.filter(imagen_horizontal__icontains=search) | qs.filter(imagen_vertical__icontains=search)
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
            context['titulo'] = 'Registro de modelo de marco'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Completa todos los campos para registrar un modelo marco'
        return context

    def form_valid(self, form):
        maluisa = form.save(commit=False)
        maluisa.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('administrador:list_modelomarialuisa')

@permission_required(perm='administrador', login_url='/webapp/login')
def modelomarialuisa_listar(request):
    template_name = 'administrador/tab_modelomarialuisa.html'
    context = {}
    context['titulo'] = 'Marialuisa'
    context['btn_nuevo'] = 'Agregar marialuisa'
    context['url_nuevo'] = reverse('administrador:nuevo_modelomarialuisa')
    context['encabezados'] = [['Id', True],
                              ['Nombre', True],
                              ['Editar', False],
                              ['Estatus', True]]
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
        'id','modelo', '', ''
    ]

    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('administrador:edit_modelomarialuisa',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><i class="material-icons">edit</i></a>'

        elif column == 'estatus':
            if row.estatus:
                return '<div class="switch"><label>Off<input type="checkbox" checked onchange=cambiar_estatus(' + str(
                    row.pk) + ')><span class="lever"></span>On</label></div>'
            else:
                return '<div class="switch"><label>Off<input type="checkbox" onchange=cambiar_estatus(' + str(
                    row.pk) + ')><span class="lever"></span>On</label></div>'

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
            context['titulo'] = 'Modificación de maria luisa'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Modifica los campos que requieras'
        return context

    def form_valid(self, form):
        # form.instance.set_password(form.cleaned_data['password'])
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('administrador:list_modelomarialuisa')



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
            context['titulo'] = 'Registro de marco'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Completa todos los campos para registrar un marco'
        return context

    def form_valid(self, form):
        maluisa = form.save(commit=False)
        maluisa.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('administrador:list_marialuisa')

@permission_required(perm='administrador', login_url='/webapp/login')
def marialuisa_listar(request):
    template_name = 'administrador/tab_marialuisa.html'
    context = {}
    context['titulo'] = 'Marialuisa'
    context['btn_nuevo'] = 'Agregar marialuisa'
    context['url_nuevo'] = reverse('administrador:nuevo_marialuisa')
    context['encabezados'] = [['Id', True],
                              ['Nombre', True],
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
                                                       'pk': row.pk}) + '"><i class="material-icons">edit</i></a>'
        elif column == 'precio':
            return "${0:,.2f}".format(row.precio)

        elif column == 'estatus':
            if row.estatus:
                return '<div class="switch"><label>Off<input type="checkbox" checked onchange=cambiar_estatus(' + str(
                    row.pk) + ')><span class="lever"></span>On</label></div>'
            else:
                return '<div class="switch"><label>Off<input type="checkbox" onchange=cambiar_estatus(' + str(
                    row.pk) + ')><span class="lever"></span>On</label></div>'

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
            context['titulo'] = 'Modificación de maria luisa'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Modifica los campos que requieras'
        return context

    def form_valid(self, form):
        # form.instance.set_password(form.cleaned_data['password'])
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('administrador:list_marialuisa')

# Clase GrosorPapel <----- Este ya no existe
class GrosorPapelCrear(PermissionRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/webapp/login'
    permission_required = 'administrador'
    model = GrosorPapel
    form_class = GrosorPapelForm
    template_name = 'config/form_1col.html'
    success_url = '/administrador/grosor_papel/listar'

    def get_context_data(self, **kwargs):
        context = super(GrosorPapelCrear, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Registro de grosor de papel'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Completa todos los campos para registrar un grosor de papel'
        return context

    def form_valid(self, form):
        grosorPapel = form.save(commit=False)
        grosorPapel.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('administrador:list_grosor_papel')

@permission_required(perm='administrador', login_url='/webapp/login')
def grosor_papel_listar(request):
    template_name = 'administrador/tab_grosor_papel.html'
    return render(request, template_name)

class GrosorPapelAjaxListView(PermissionRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/webapp/login'
    permission_required = 'administrador'
    model = GrosorPapel
    columns = [
        'medida', 'editar'
    ]

    order_columns = [
    'medida', ''
    ]

    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('administrador:edit_grosor_papel',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><i class="material-icons">edit</i></a>'

        elif column == 'estatus':
            if row.estatus:
                return '<div class="switch"><label>Off<input type="checkbox" checked onchange=cambiar_estatus(' + str(
                    row.pk) + ')><span class="lever"></span>On</label></div>'
            else:
                return '<div class="switch"><label>Off<input type="checkbox" onchange=cambiar_estatus(' + str(
                    row.pk) + ')><span class="lever"></span>On</label></div>'

        elif column == 'imagen':
                if row.imagen.url:
                    return '<img style="width:100%" src="'+ row.imagen.url +'" />'


        return super(GrosorPapelAjaxListView, self).render_column(row, column)

    def get_initial_queryset(self):
        return GrosorPapel.objects.all()


class GrosorPapelActualizar(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/webapp/login'
    permission_required = 'administrador'
    model = GrosorPapel
    template_name = 'config/form_1col.html'
    form_class = GrosorPapelForm

    def get_context_data(self, **kwargs):
        context = super(GrosorPapelActualizar, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Modificación de maria luisa'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Modifica los campos que requieras'
        return context

    def form_valid(self, form):
        # form.instance.set_password(form.cleaned_data['password'])
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('administrador:list_grosor_papel')

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
        tipoPapel = form.save(commit=False)
        tipoPapel.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('administrador:list_tipo_papel')

@permission_required(perm='administrador', login_url='/webapp/login')
def tipo_papel_listar(request):
    template_name = 'administrador/tab_tipo_papel.html'
    context = {}
    context['titulo'] = 'Tipo de papel'
    context['btn_nuevo'] = 'Agregar papel'
    context['url_nuevo'] = reverse('administrador:nuevo_tipo_papel')
    context['encabezados'] = [['Grosor', True],
                              ['Precio', True],
                              ['Editar', False],
                              ['Estatus', True]]
    context['url_ajax'] = reverse('administrador:tab_list_tipo_papel')
    context['url_update_estatus'] = '/administrador/tipo_papel/cambiar_estatus/'


    return render(request, template_name, context)

class TipoPapelAjaxListView(PermissionRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/webapp/login'
    permission_required = 'administrador'
    model = GrosorPapel
    columns = [
        'grosor', 'precio',  'editar', 'estatus'
    ]

    order_columns = [
        'grosor', 'precio', '', ''
    ]

    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('administrador:edit_tipo_papel',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><i class="material-icons">edit</i></a>'
        elif column == 'precio':
            return "${0:,.2f}".format(row.precio)

        elif column == 'estatus':
            if row.estatus:
                return '<div class="switch"><label>Off<input type="checkbox" checked onchange=cambiar_estatus(' + str(
                    row.pk) + ')><span class="lever"></span>On</label></div>'
            else:
                return '<div class="switch"><label>Off<input type="checkbox" onchange=cambiar_estatus(' + str(
                    row.pk) + ')><span class="lever"></span>On</label></div>'

        elif column == 'imagen':
                if row.imagen.url:
                    return '<img style="width:100%" src="'+ row.imagen.url +'" />'


        return super(TipoPapelAjaxListView, self).render_column(row, column)

    def get_initial_queryset(self):
        return TipoPapel.objects.all()

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(grosor__icontains=search) | qs.filter(precio__icontains=search)
        return qs

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
            context['titulo'] = 'Modificación de tipo papel'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Modifica los campos que requieras'
        return context

    def form_valid(self, form):
        # form.instance.set_password(form.cleaned_data['password'])
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('administrador:list_tipo_papel')

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
            context['titulo'] = 'Registro de tipo de textura'
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
    template_name = 'administrador/tab_textura.html'
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
                                                       'pk': row.pk}) + '"><i class="material-icons">edit</i></a>'

        elif column == 'estatus':
            if row.estatus:
                return '<div class="switch"><label>Off<input type="checkbox" checked onchange=cambiar_estatus(' + str(
                    row.pk) + ')><span class="lever"></span>On</label></div>'
            else:
                return '<div class="switch"><label>Off<input type="checkbox" onchange=cambiar_estatus(' + str(
                    row.pk) + ')><span class="lever"></span>On</label></div>'

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
            context['titulo'] = 'Modificación de tipo papel'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Modifica los campos que requieras'
        return context

    def form_valid(self, form):
        # form.instance.set_password(form.cleaned_data['password'])
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('administrador:list_textura')

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
            context['titulo'] = 'Registro de tipo de logo'
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
    template_name = 'administrador/tab_logo.html'
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
                                                       'pk': row.pk}) + '"><i class="material-icons">edit</i></a>'

        elif column == 'estatus':
            if row.estatus:
                return '<div class="switch"><label>Off<input type="checkbox" checked onchange=cambiar_estatus(' + str(
                    row.pk) + ')><span class="lever"></span>On</label></div>'
            else:
                return '<div class="switch"><label>Off<input type="checkbox" onchange=cambiar_estatus(' + str(
                    row.pk) + ')><span class="lever"></span>On</label></div>'

        elif column == 'imagen':
                if row.imagen.url:
                    return '<img style="width:80%" src="'+ row.imagen.url +'" />'


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
    template_name = 'administrador/tab_MenuFotopartner.html'
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
                                                       'pk': row.pk}) + '"><i class="material-icons">edit</i></a>'

        elif column == 'estatus':
            if row.estatus:
                return '<div class="switch"><label>Off<input type="checkbox" checked onchange=cambiar_estatus(' + str(
                    row.pk) + ')><span class="lever"></span>On</label></div>'
            else:
                return '<div class="switch"><label>Off<input type="checkbox" onchange=cambiar_estatus(' + str(
                    row.pk) + ')><span class="lever"></span>On</label></div>'

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

# Clase Promocion
class PromocionCrear(PermissionRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/webapp/login'
    permission_required = 'administrador'
    model = Promocion
    form_class = PromocionForm
    template_name = 'config/registro_promo.html'
    success_url = '/administrador/Promocion/listar'

    def get_context_data(self, **kwargs):
        context = super(PromocionCrear, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Registro de Promocion'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Completa todos los campos para registrar una Promocion'
        return context

    def form_valid(self, form):
        menu = form.save(commit=False)
        menu.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('administrador:list_Promocion')

@permission_required(perm='administrador', login_url='/webapp/login')
def Promocion_listar(request):
    template_name = 'administrador/tab_Promocion.html'
    context = {}
    context['titulo'] = 'Promocion'
    context['btn_nuevo'] = 'Agregar Promocion'
    context['url_nuevo'] = reverse('administrador:nuevo_Promocion')
    context['encabezados'] = [['Url', True],
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
        'url', 'editar', 'estatus'
    ]

    order_columns = [
        'url', '', ''
    ]

    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('administrador:edit_Promocion',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><i class="material-icons">edit</i></a>'

        elif column == 'estatus':
            if row.estatus:
                return '<div class="switch"><label>Off<input type="checkbox" checked onchange=cambiar_estatus(' + str(
                    row.pk) + ')><span class="lever"></span>On</label></div>'
            else:
                return '<div class="switch"><label>Off<input type="checkbox" onchange=cambiar_estatus(' + str(
                    row.pk) + ')><span class="lever"></span>On</label></div>'

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
    template_name = 'config/registro_promo.html'
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
            return row.fecha_compra.astimezone(self.settingstime_zone).strftime("%d-%b-%Y %H:%M")
        elif column == 'direccion':
            return row.direccion.direccion_completa()
        elif column == 'total':
            return "$" + "{0:,.2f}".format(row.total)
        elif column == 'detalle_pago':
            return '*******423'
        return super(VentasAjaxListView, self).render_column(row, column)

    def get_initial_queryset(self):
        return Orden.objects.all()

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
            return '<a class="" href ="#"><i class="fa fa-users"></i></a>'
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
    context['titulo'] = 'Usuarios generales'
    context['encabezados'] = [['ID', True],
                              ['Nombre', True],
                              ['Correo', True],
                              ['Confiable', True],
                              ['Estatus', True],
                              ['Detalle', False],
                              ]
    context['url_ajax'] = reverse('administrador:tab_list_fotopartners')
    context['url_update_estatus'] = '/administrador/fotografo/cambiar_estatus/'
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
            return '<a class="" href ="#"><i class="fa fa-users"></i></a>'
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