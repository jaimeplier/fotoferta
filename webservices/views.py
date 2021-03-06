from django.contrib.auth import login as auth_login
from django.utils import timezone
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from config.models import Contactanos, Categoria, Colonia, RedSocial, Usuario, UsuarioRedSocial, Fotografo, Rol, Logo, \
    Promocion
from webservices.Permissions import FotopartnerPermission
from webservices.serializers import ContactanosSerializer, CategoriasSerializer, ColoniaSerializer, RedSocialSerializer, \
    LoginSerializer, RegistroRedesSerializer, LogoSerializer, FotoPerfilSerializer, FotoPortadaSerializer, \
    PromocionBannerSerializer


class ListContactanos(ListAPIView):

    serializer_class = ContactanosSerializer

    def get_queryset(self):
        queryset = Contactanos.objects.all()
        return queryset

class ListDatosCP(ListAPIView):
    """
            **Parámetros**

            1. cp: Código postal a buscar

    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SessionAuthentication, TokenAuthentication)

    serializer_class = ColoniaSerializer

    def get_queryset(self):
        cp = self.request.query_params.get('cp', None)
        queryset = Colonia.objects.none()
        if cp is not None:
            queryset = Colonia.objects.filter(cp=cp)
        return queryset

class ListRedesSociales(ListAPIView):

    serializer_class = RedSocialSerializer

    def get_queryset(self):
        queryset = RedSocial.objects.all()
        return queryset

class Signin(APIView):
    """
    post:
        Registro con redes sociales
    """


    def post(self, request):
        response_data = {}
        serializer = RegistroRedesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        nombre = serializer.data.get('nombre')
        correo = serializer.data.get('correo')
        red_social = serializer.data.get('red_social')
        token = serializer.data.get('token')

        red_social = RedSocial.objects.get(pk=red_social)
        user = None
        if Usuario.objects.filter(correo=correo).exists():
            user = Usuario.objects.get(correo=correo)
            if UsuarioRedSocial.objects.filter(usuario=user, red_social=red_social).exists():
                response_data['resultado'] = 1
                response_data['error'] = "Ya existe un usuario registrado"
                return Response(response_data)
            UsuarioRedSocial.objects.create(usuario=user, red_social=red_social, token=token)
            auth_login(request, user)


        elif user is None:
            rol = Rol.objects.get(pk=3) # Rol fotopartner
            fotografo = Fotografo.objects.create(nombre=nombre, correo=correo, password='F-t_f3rTas?57',
                                                 rol=rol, terminos_condiciones=True)
            pswd = Fotografo.objects.make_random_password(length=16)
            user = Usuario.objects.get(pk=fotografo.pk)
            user.set_password(pswd)
            user.save()
            UsuarioRedSocial.objects.create(usuario=user, red_social=red_social, token=token)
            auth_login(request, user)
        response_data['resultado'] = 0
        response_data['exito'] = 'Registro exitoso'
        return Response(response_data, status=status.HTTP_200_OK)

    def get_serializer(self):
        return RegistroRedesSerializer()

class Login(APIView):
    """
    post:
        Login con redes sociales
    """


    def post(self, request):
        response_data = {}
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        correo = serializer.data.get('correo')
        red_social = serializer.data.get('red_social')
        token = serializer.data.get('token')

        red_social = RedSocial.objects.get(pk=red_social)
        user = None
        if Usuario.objects.filter(correo=correo).exists():
            user = Usuario.objects.get(correo=correo)
            if UsuarioRedSocial.objects.filter(usuario=user, red_social=red_social).exists():
                try:
                    usuario_red = UsuarioRedSocial.objects.get(usuario=user, red_social=red_social,token=token)
                    auth_login(request, user)
                except:
                    response_data['resultado'] = 1
                    response_data['error'] = "Usuario y/o contraseña incorrectos"
                    return Response(response_data)
            else:
                response_data['resultado'] = 1
                response_data['error'] = "Usuario y/o contraseña incorrectos"
                return Response(response_data)
        else:
            response_data['resultado'] = 1
            response_data['error'] = "Usuario y/o contraseña incorrectos"
            return Response(response_data)

        response_data['resultado'] = 0
        response_data['exito'] = 'Login realizado correctamente'
        return Response(response_data, status=status.HTTP_200_OK)

    def get_serializer(self):
        return LoginSerializer()

class ListLogo(ListAPIView):

    serializer_class = LogoSerializer

    def get_queryset(self):
        queryset = Logo.objects.filter(estatus=True)
        return queryset

class CambiarFotoPerfil(APIView):
    """
    post:
        Cambiar Foto de perfil
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def post(self, request):
        response_data = {}
        serializer = FotoPerfilSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        foto = serializer.validated_data.get('foto')

        user = Usuario.objects.get(pk=self.request.user.pk)
        user.foto_perfil = foto
        user.save()
        response_data['resultado'] = 0
        response_data['exito'] = 'Foto de perfil actualizada correctamente'
        return Response(response_data, status=status.HTTP_200_OK)

    def get_serializer(self):
        return FotoPerfilSerializer()

class CambiarFotoPortada(APIView):
    """
    post:
        Cambiar Foto de portada
    """
    permission_classes = (IsAuthenticated, FotopartnerPermission)
    authentication_classes = (SessionAuthentication,)

    def post(self, request):
        response_data = {}
        serializer = FotoPortadaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        foto = serializer.validated_data.get('foto')

        user = Fotografo.objects.get(pk=self.request.user.pk)
        user.foto_portada = foto
        user.save()
        response_data['resultado'] = 0
        response_data['exito'] = 'Foto de portada actualizada correctamente'
        return Response(response_data, status=status.HTTP_200_OK)

    def get_serializer(self):
        return FotoPortadaSerializer()

class ListPromocionesBanner(ListAPIView):

    serializer_class = PromocionBannerSerializer

    def get_queryset(self):
        queryset = Promocion.objects.filter(estatus=True, fecha_fin__gte=timezone.now()).order_by('-fecha_inicio')
        return queryset