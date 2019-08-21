from django.db import transaction
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from config.models import Fotografia, FotoReaccion, Reaccion, Fotografo
from webservices.Permissions import FotopartnerPermission
from webservices.serializers import FotoReaccionSerializer, AddFavoritoSerializer


class ListFavoritos(ListAPIView):
    permission_classes = (IsAuthenticated, FotopartnerPermission)
    authentication_classes = (SessionAuthentication,)

    serializer_class = FotoReaccionSerializer

    def get_queryset(self):
        queryset = FotoReaccion.objects.filter(usuario=self.request.user, reaccion__nombre='Favorito', foto__estatus=True)
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
                foto.likes += 1
                foto.save()
                FotoReaccion.objects.create(foto=foto, usuario=cliente, reaccion=reaccion)
            return Response({'exito': 'Se ha agregado a favoritos'}, status=status.HTTP_200_OK)
        return Response({'error': 'Ocurrio un error'}, status=status.HTTP_200_OK)


    def get_serializer(self):
        return AddFavoritoSerializer()