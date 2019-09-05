from django.db import transaction
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from config.models import Fotografia, FotoReaccion, Reaccion, Fotografo, SiguiendoFotografo, Notificacion
from webservices.Pagination import SmallPagesPagination, SmallestPagesPagination
from webservices.Permissions import FotopartnerPermission
from webservices.serializers import FotoReaccionSerializer, AddFavoritoSerializer, FotoparterSiguiendoSerializer, \
    AddSeguidorSerializer, FotografoSerializer, NotificacionSerializer


class ListFavoritos(ListAPIView):
    permission_classes = (IsAuthenticated, FotopartnerPermission)
    authentication_classes = (SessionAuthentication,)
    pagination_class = SmallPagesPagination

    serializer_class = FotoReaccionSerializer

    def get_queryset(self):
        queryset = FotoReaccion.objects.filter(usuario=self.request.user, reaccion__nombre='Favorito', foto__estatus=True).order_by('-fecha_alta')
        return queryset

class AgregarFavoritos(APIView):
    permission_classes = (IsAuthenticated, FotopartnerPermission)
    authentication_classes = (SessionAuthentication,)

    def post(self, request):
        serializer = AddFavoritoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cliente = Fotografo.objects.get(pk=request.user.pk)

        # ---> OBTENER FOTOGRAFIA <---

        foto = Fotografia.objects.get(pk=serializer.validated_data['foto'])
        like = serializer.validated_data['like']

        # ---> Buscar si ya existe en las reacciones <---
        foto_reaccion = FotoReaccion.objects.filter(foto=foto, usuario=cliente)
        num_fotos = len(foto_reaccion)
        if num_fotos >0 and like==False:
            foto_reaccion.delete()
            foto.likes -=1
            foto.save()
            return Response({'exito': 'Se ha eliminado la foto de favoritos'}, status=status.HTTP_200_OK)
        elif num_fotos ==0 and like==True:
            with transaction.atomic():
                reaccion = Reaccion.objects.get(nombre='Favorito')
                # Buscar notificacion y/o crearla
                receiver = Fotografo.objects.get(pk=foto.usuario.pk)
                notificacion = Notificacion.objects.filter(actioner=cliente, reaccion=reaccion, receiver=receiver, foto=foto)
                if not notificacion.exists():
                    Notificacion.objects.create(actioner=cliente, reaccion=reaccion, receiver=receiver, foto=foto)

                foto.likes += 1
                foto.save()
                FotoReaccion.objects.create(foto=foto, usuario=cliente, reaccion=reaccion)
            return Response({'exito': 'Se ha agregado a favoritos'}, status=status.HTTP_200_OK)
        return Response({'error': 'Ocurrio un error'}, status=status.HTTP_200_OK)


    def get_serializer(self):
        return AddFavoritoSerializer()

class ListSiguiendo(ListAPIView):
    permission_classes = (IsAuthenticated, FotopartnerPermission)
    authentication_classes = (SessionAuthentication,)
    pagination_class = SmallPagesPagination

    serializer_class = FotoparterSiguiendoSerializer

    def get_queryset(self):
        fotografo = Fotografo.objects.get(pk=self.request.user.pk)
        queryset = SiguiendoFotografo.objects.filter(fotografo=fotografo, siguiendo_a__estatus=True).order_by('siguiendo_a__nombre')
        return queryset

class SeguirFotopartner(APIView):
    permission_classes = (IsAuthenticated, FotopartnerPermission)
    authentication_classes = (SessionAuthentication,)

    def post(self, request):
        serializer = AddSeguidorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        seguidor = Fotografo.objects.get(pk=request.user.pk)

        # ---> OBTENER FOTOGRAFIA <---

        fotografo = Fotografo.objects.get(pk=serializer.validated_data['fotopartner'])
        seguir = serializer.validated_data['seguir']

        # ---> Buscar si ya existe en los seguidores <---
        fotografo_siguiendo = SiguiendoFotografo.objects.filter(fotografo=seguidor, siguiendo_a=fotografo)
        num_seguidor_fotopart = len(fotografo_siguiendo)
        if num_seguidor_fotopart >0 and seguir==False:
            fotografo_siguiendo.delete()
            fotografo.seguidores -=1
            fotografo.save()
            return Response({'exito': 'Has dejado de seguir al Fotopartner'}, status=status.HTTP_200_OK)
        elif num_seguidor_fotopart ==0 and seguir==True:
            with transaction.atomic():
                # Buscar notificacion y/o crearla
                reaccion = Reaccion.objects.get(nombre='Siguiendo')
                notificacion = Notificacion.objects.filter(actioner=seguidor, reaccion=reaccion, receiver=fotografo, foto=None)
                if not notificacion.exists():
                    Notificacion.objects.create(actioner=seguidor, reaccion=reaccion, receiver=fotografo)

                fotografo.seguidores += 1
                fotografo.save()
                SiguiendoFotografo.objects.create(fotografo=seguidor, siguiendo_a=fotografo)
            return Response({'exito': 'Siguiendo a Fotopartner'}, status=status.HTTP_200_OK)
        return Response({'error': 'Ocurrio un error'}, status=status.HTTP_200_OK)


    def get_serializer(self):
        return AddSeguidorSerializer()

class ListFotopartners(ListAPIView):
    permission_classes = (IsAuthenticated, FotopartnerPermission)
    authentication_classes = (SessionAuthentication,)
    pagination_class = SmallPagesPagination

    serializer_class = FotografoSerializer

    def get_queryset(self):
        queryset = Fotografo.objects.filter(estatus=True).order_by('nombre')
        return queryset

class ListNotificaciones(ListAPIView):
    permission_classes = (IsAuthenticated, FotopartnerPermission)
    authentication_classes = (SessionAuthentication,)
    pagination_class = SmallestPagesPagination

    serializer_class = NotificacionSerializer

    def get_queryset(self):
        fotografo = Fotografo.objects.get(pk=self.request.user.pk)
        queryset = Notificacion.objects.filter(receiver=fotografo).order_by('fecha_creacion')
        return queryset