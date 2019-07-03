from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.views.generic import CreateView, UpdateView
from django_datatables_view.base_datatable_view import BaseDatatableView

from administrador.forms import CodigoMarcoForm, TamanioForm, MarcoForm, MarialuisaForm
from config.models import CodigoMarco, Tamanio, Marco, MariaLuisa


class CodigoMarcoCrear(CreateView):
    redirect_field_name = 'next'
    login_url = '/webapp/'
    permission_required = ''
    model = CodigoMarco
    form_class = CodigoMarcoForm
    template_name = 'config/form_1col.html'
    # success_url = '/administrador/codigo_marco/nuevo'

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



# @permission_required(perm='admin_sitio', login_url='/webapp/')
def codigo_marco_listar(request):
    template_name = 'administrador/tab_codigo_marco.html'
    return render(request, template_name)


class CodigoMarcoListarAjaxListView(BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/webapp/'
    # permission_required = 'admin_sitio'
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


class CodigoMarcoActualizar(UpdateView):
    # redirect_field_name = 'next'
    # login_url = '/webapp/'
    # permission_required = 'admin_sitio'
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

class TamanioCrear(CreateView):
    # redirect_field_name = 'next'
    # login_url = '/webapp/'
    permission_required = ''
    model = Tamanio
    form_class = TamanioForm
    template_name = 'config/form_1col.html'
    # success_url = '/administrador/tamanio/nuevo'

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

def tamanio_listar(request):
    template_name = 'administrador/tab_tamanio.html'
    return render(request, template_name)

class TamanioListarAjaxListView(BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/webapp/'
    # permission_required = 'admin_sitio'
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


class TamanioActualizar(UpdateView):
    # redirect_field_name = 'next'
    # login_url = '/webapp/'
    # permission_required = 'admin_sitio'
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

class MarcoCrear(CreateView):
    # redirect_field_name = 'next'
    # login_url = '/webapp/'
    permission_required = ''
    model = Marco
    form_class = MarcoForm
    template_name = 'config/form_1col.html'
    # success_url = '/administrador/tamanio/nuevo'

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

def marco_listar(request):
    template_name = 'administrador/tab_marco.html'
    return render(request, template_name)

class MarcoListarAjaxListView(BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/webapp/'
    # permission_required = 'admin_sitio'
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


class MarcoActualizar(UpdateView):
    # redirect_field_name = 'next'
    # login_url = '/webapp/'
    # permission_required = 'admin_sitio'
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


# Clase Marialuisa
'''


class MarialuisaCrear(CreateView):
    # redirect_field_name = 'next'
    # login_url = '/webapp/'
    permission_required = ''
    model = MariaLuisa
    form_class = MarialuisaForm
    template_name = 'config/form_1col.html'
    # success_url = '/administrador/marialuisa/nuevo'

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

def marialuisa_listar(request):
    template_name = 'administrador/tab_marialuisa.html'
    return render(request, template_name)

class MarialuisaAjaxListView(BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/webapp/'
    # permission_required = 'admin_sitio'
    model = MariaLuisa
    columns = [
        'nombre'
    #    'modelo', 'precio', 'tamanio', 'imagen', 'editar', 'estatus'
    ]

    order_columns = [
    'nombre'
    #    'modelo', 'precio', 'tamanio', 'imagen', '', ''
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

        return super(MarcoListarAjaxListView, self).render_column(row, column)

    def get_initial_queryset(self):
        return Marco.objects.all()


class MarialuisaActualizar(UpdateView):
    # redirect_field_name = 'next'
    # login_url = '/webapp/'
    # permission_required = 'admin_sitio'
    model = MariaLuisa
    template_name = 'config/form_1col.html'
    form_class = MarialuisaForm

    def get_context_data(self, **kwargs):
        context = super(MarialuisaActualizar, self).get_context_data(**kwargs)
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
        return reverse('administrador:list_marialuisa')
'''


