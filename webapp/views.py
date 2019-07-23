from django.contrib.auth import authenticate, login as auth_login, logout
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import CreateView

from config.models import Fotografo, Rol, Fotografia
from webapp.forms import RegistroForm


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
                user = form.save(commit=False)
                user.rol = rol
                user.set_password(user.password)
                user.save()

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

                return redirect(reverse('webapp:sitio_en_construccion'))
            except:
                return render(self.request, template_name=self.template_name,
                              context={'form': form,
                                       'error_message': 'Ocurrió un error en el registro, intenta mas tarde o con otro correo'})
        else:
            return self.render_to_response(self.get_context_data(form=form))


def vista_perfil(request):
    template_name = 'cliente/perfil.html'
    return render(request, template_name)

def vista_carrito(request):
    template_name = 'cliente/carrito.html'
    return render(request, template_name)

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

def vista_marco(request):
    template_name = 'cliente/marco.html'
    return render(request, template_name)

def vista_exclusivas(request):
    template_name = 'cliente/exclusivas.html'
    return render(request, template_name)