from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
# Create your views here.
from django.urls import reverse
from django.views.generic import CreateView, UpdateView

from administrador.forms import (CodigoMarcoForm, MarcoForm, MarialuisaForm,
                                 TamanioForm, ModeloMarialuisaForm)
from config.models import (CodigoMarco, Marco, MariaLuisa, ModeloMariaLuisa,
                           Tamanio)
from django_datatables_view.base_datatable_view import BaseDatatableView


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
    template_name = 'administrador/tab_codigo_marco.html'
    return render(request, template_name)


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
    return render(request, template_name)

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
    template_name = 'administrador/tab_marco.html'
    return render(request, template_name)

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
            context['titulo'] = 'Modificación de tamaño'
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
    return render(request, template_name)

class ModeloMarialuisaAjaxListView(PermissionRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/webapp/login'
    permission_required = 'administrador'
    model = ModeloMariaLuisa
    columns = [
        'modelo', 'editar'
    ]

    order_columns = [
    'modelo', ''
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
    return render(request, template_name)

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
