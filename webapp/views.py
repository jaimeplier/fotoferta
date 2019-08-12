from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, DetailView
from django.http import HttpResponseRedirect, JsonResponse

from config.models import Fotografo, Rol, Fotografia, Direccion, Producto
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
                # sendMail(to, 'Registro inderspace', message)
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
    template_name = 'config/form_1col.html'
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
        logo = form.save(commit=False)
        logo.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('webapp:direccion')

@permission_required(perm='fotopartner', login_url='/webapp/login')
def direccion_listar(request):
    template_name = 'config/tab_base.html'
    context = {}
    context['titulo'] = 'Direccion'
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
        return Direccion.objects.all()


class DireccionActualizar(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/webapp/login'
    permission_required = 'fotopartner'
    model = Direccion
    template_name = 'config/form_1col.html'
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
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('webservices:list_direccion')

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
    return render(request, template_name)

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

def vista_editar_perfil(request):
    template_name = 'cliente/editar_perfil.html'
    return render(request, template_name)

def vista_marco(request, producto):
    template_name = 'cliente/marco.html'
    prod = Producto.objects.get(pk=producto)
    context = {'producto': prod}
    return render(request, template_name, context)

def vista_exclusivas(request):
    template_name = 'cliente/exclusivas.html'
    return render(request, template_name)