from django.contrib.auth import authenticate, login as auth_login, logout
from django.shortcuts import render, redirect
from django.urls import reverse


def login(request):
    error_message = ''
    if request.user.is_authenticated:
        return redirect(reverse('webapp:list_chofer'))
    if request.method == 'POST':
        correo = request.POST['correo']
        password = request.POST['password']
        user = authenticate(correo=correo, password=password)
        if user is not None:
            if user.estatus:
                auth_login(request, user)
                if request.POST.get('next') is not None:
                    return redirect(request.POST.get('next'))
                elif user.rol.pk == 2: # Administrador Fotofertas
                    return redirect(reverse('administrador:list_marco'))
                # elif user.rol.pk in [3,4]: # Cliente o Fotopartner
                #     return redirect(reverse('webapp:'))
                logout(request)
                return redirect(reverse('webapp:login_unauthorized'))
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