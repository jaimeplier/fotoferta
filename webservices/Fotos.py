from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from config.models import Fotografia, TipoFoto, Orientacion, Tamanio, Fotografo, Etiqueta
from webservices.Pagination import SmallPagesPagination
from webservices.Permissions import FotopartnerPermission
from webservices.serializers import RegistroFotografiaSerializer, FotografiaSerializer


class SubirFotografia(APIView):
    permission_classes = (IsAuthenticated, FotopartnerPermission)
    authentication_classes = (SessionAuthentication,)

    def post(self, request):
        serializer = RegistroFotografiaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # ---> DATOS DE FOTOGRAFIA <---

        tipo_venta_foto = serializer.validated_data['tipo_venta_foto']
        categoria = serializer.validated_data['categoria']
        nombre = serializer.validated_data['nombre']
        descripcion = serializer.validated_data['descripcion']
        etiquetas = serializer.validated_data['etiquetas']
        foto_original = serializer.validated_data['foto']
        foto_muestra = serializer.validated_data['foto']

        # list de etiquetas
        etiquetas = etiquetas.split(',')
        etiquetas_objts = []
        for etiqueta in etiquetas:
            etiquetas_objts.append(Etiqueta.objects.get(pk=etiqueta))

        # Revisar tipo de imagen
        tipo_foto = TipoFoto.objects.get(pk=1)
        if tipo_venta_foto == 3:
            tipo_foto = TipoFoto.objects.get(pk=2)

        # Revisar orientacion
        orientacion = Orientacion.objects.get(pk=1)

        # Revisar tamaño de fotografia
        tamanio = Tamanio.objects.get(pk=1)

        usuario = self.request.user
        alto_foto = 1234
        ancho_foto = 1234

        # revisar precio fotografía

        precio = 0
        if tipo_venta_foto == 2:
            # Precio foto normal revisando tamaño
            precio = 100
        elif tipo_venta_foto == 3:
            # Precio foto exclusiva revisando tamaño
            precio = 200

        # Aprobacion de fotografia por ser fotopartner
        fotografo = Fotografo.objects.get(pk=self.request.user.pk)
        aprobada = False
        if fotografo.is_fotopartner:
            aprobada = True

        # ---> REGISTRO DE Fotografia<---
        foto = Fotografia.objects.create(nombre = nombre, usuario= usuario, foto_original=foto_original,
                                         foto_muestra=foto_muestra, descripcion=descripcion, alto=alto_foto,
                                         ancho=ancho_foto, tipo_foto=tipo_foto, orientacion=orientacion, tamanio=tamanio,
                                         precio = precio, aprobada=aprobada)


        return Response({'exito': 'registro exitoso'}, status=status.HTTP_200_OK)


    def get_serializer(self):
        return RegistroFotografiaSerializer()

class ListFotosHome(ListAPIView):

    serializer_class = FotografiaSerializer
    pagination_class = SmallPagesPagination

    def get_queryset(self):
        queryset = Fotografia.objects.all().order_by('?')
        return queryset

class ListMisFotos(ListAPIView):

    serializer_class = FotografiaSerializer

    def get_queryset(self):
        queryset = Fotografia.objects.filter(usuario=self.request.user).order_by('-fecha_alta')
        return queryset
