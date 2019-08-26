from PIL import Image
from io import BytesIO
import sys

from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from config.models import Fotografia, TipoFoto, Orientacion, Tamanio, Fotografo, Etiqueta, Categoria, FotoPrecio
from webservices.Pagination import SmallPagesPagination, SmallestPagesPagination
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
        #publica = serializer.validated_data['publica']
        publica = True

        # list de etiquetas
        etiquetas = etiquetas.split(',')
        etiquetas_objts = []
        for etiqueta in etiquetas:
            try:
                etiquetas_objts.append(Etiqueta.objects.get(pk=etiqueta))
            except:
                nva_etiqueta = Etiqueta.objects.create(nombre=etiqueta)
                etiquetas_objts.append(nva_etiqueta)

        # list de categorias
        categorias = categoria.split(',')
        categorias_objts = []
        for categoria in categorias:
            categorias_objts.append(Categoria.objects.get(pk=categoria))

        # Revisar tipo de imagen
        if publica or tipo_venta_foto==1 or tipo_venta_foto==2:
            tipo_foto = TipoFoto.objects.get(pk=1)
        else:
            tipo_foto = TipoFoto.objects.get(pk=2)

        # Revisar orientacion
        altura_foto = foto_original.image.height
        ancho_foto = foto_original.image.width
        if altura_foto > ancho_foto:
            orientacion = Orientacion.objects.get(pk=2)  # Vertical
            # invertir valores de variables para comparar con tamaños del sistema
            altura_vertical = ancho_foto
            ancho_vertical = altura_foto

        else:
            orientacion = Orientacion.objects.get(pk=1)  # Horizontal

        # Revisar tamaño de fotografia
        area_foto = altura_foto * ancho_foto
        tam_precios = FotoPrecio.objects.filter(tipo_foto=tipo_foto, tamanio__estatus=True) # Filtro de tam foto por tipo de foto
        mas_chico = tam_precios.order_by('min_area').first()
        mas_grande = tam_precios.order_by('-max_area').first()
        if area_foto < mas_chico.min_area or area_foto > mas_grande.max_area:
            return Response({
                'error': 'No se puede guardar la imagen porque no se pudo categorizar su tamaño. Los limites de tamaño son: min {}x{} px. y máx {}x{} px.'.format(
                    mas_chico.min_ancho, mas_chico.min_altura, mas_grande.max_ancho, mas_grande.max_altura)},
                status=status.HTTP_406_NOT_ACCEPTABLE)
        # (max_area__gte=5992704, min_area__lte=5992704)
        tama = tam_precios.filter(max_area__gte=area_foto)
        # tama2 = tama.filter(min_area__gte=area_foto)
        if orientacion.pk == 2: # si es vertical compara con altura y ancho invertido
            tama.filter(min_ancho__gte=ancho_vertical, max_ancho__lte=ancho_vertical)
            tama.filter(min_altura__gte=altura_vertical, max_altura__lte=altura_vertical)
        else:
            tama.filter(min_ancho__gte=ancho_foto, max_ancho__lte=ancho_foto)
            tama.filter(min_altura__gte=altura_foto, max_altura__lte=altura_foto)

        # Si no se categoriza la imagen en tamaño se regresa un error
        if len(tama)<=0:
            return Response({'error': 'No se puede guardar la imagen porque no se pudo categorizar su tamaño.'}, status=status.HTTP_406_NOT_ACCEPTABLE)

        tama.order_by('min_area') # Se ordena por tamaños de menor a mayor
        foto_precio = tama.first() # Se toma el tamaño mas pequeño (FotoPrecio)
        tamanio = foto_precio.tamanio

        usuario = self.request.user

        # Asignar precio fotografía
        precio = 0
        if tipo_venta_foto == 2 or tipo_venta_foto == 3:
            # Precio foto normal o exclusiva
            precio = foto_precio.precio

        # Aprobacion de fotografia por ser fotopartner
        fotografo = Fotografo.objects.get(pk=self.request.user.pk)
        aprobada = False
        if fotografo.is_fotopartner:
            aprobada = True

        # Valores de redimensionamiento de imagen muestra
        reduccion_tamanio = 0.3
        tamanio_horizontal_muestra = foto_original.image.width * reduccion_tamanio
        tamanio_vertical_muestra = foto_original.image.height * reduccion_tamanio

        # Copiar foto original
        foto_muestra = foto_original

        import os
        module_dir = os.path.dirname(__file__)
        archivo_wm = os.path.join(module_dir, 'marca_agua_f.png')
        marca_agua = Image.open(archivo_wm) # Abrir archivo de marca de agua

        imagen_temporal = Image.open(foto_muestra)
        outputIoStream = BytesIO()
        outputIoStream_home = BytesIO()

        # Redimensionamiento de imagen
        imagen_temporal_redimensionada = imagen_temporal.resize((int(tamanio_horizontal_muestra), int(tamanio_vertical_muestra)))

        # Guarda flujo de datos para foto home sin marca de agua
        foto_home = imagen_temporal_redimensionada
        imagen_temporal_redimensionada.save(outputIoStream_home, format='JPEG')
        outputIoStream_home.seek(0)
        foto_home = InMemoryUploadedFile(outputIoStream_home, 'ImageField',
                                            "%s.jpg" % foto_muestra.name.split('.')[0], 'image/jpeg',
                                            sys.getsizeof(outputIoStream_home), None)
        # Marca de agua en mosaico
        for left in range(0, imagen_temporal_redimensionada.width, marca_agua.width):
            for top in range(0, imagen_temporal_redimensionada.height, marca_agua.height):
                imagen_temporal_redimensionada.paste(marca_agua, (left, top),marca_agua)

        # Guarda flujo de datos
        imagen_temporal_redimensionada.save(outputIoStream, format='JPEG')
        outputIoStream.seek(0)
        foto_muestra = InMemoryUploadedFile(outputIoStream, 'ImageField',
                                               "%s.jpg" % foto_muestra.name.split('.')[0], 'image/jpeg',
                                               sys.getsizeof(outputIoStream), None)

        # ---> REGISTRO DE FOTOGRAFIA<---
        foto = Fotografia.objects.create(nombre = nombre, usuario= usuario, foto_original=foto_original,
                                         foto_muestra=foto_muestra, foto_home=foto_home, descripcion=descripcion, alto=altura_foto,
                                         ancho=ancho_foto, tipo_foto=tipo_foto, orientacion=orientacion, tamanio=tamanio,
                                         precio = precio, aprobada=aprobada)
        foto.categorias.add(*categorias_objts)
        foto.etiquetas.add(*etiquetas_objts)


        return Response({'exito': 'registro exitoso'}, status=status.HTTP_200_OK)


    def get_serializer(self):
        return RegistroFotografiaSerializer()

class ListFotosHome(ListAPIView):

    serializer_class = FotografiaSerializer
    pagination_class = SmallPagesPagination

    def get_queryset(self):
        queryset = Fotografia.objects.filter(publica=True, aprobada=True, estatus=True).order_by('?')
        return queryset

class ListFotosRecomendadas(ListAPIView):
    """
            **Parámetros**

            1. foto: ID de la foto seleccionada para listar categorias iguales a la seleccionada

            """
    serializer_class = FotografiaSerializer
    pagination_class = SmallestPagesPagination

    def get_queryset(self):
        foto_pk = self.request.query_params.get('foto', None)
        if foto_pk is not None:
            foto = Fotografia.objects.get(pk=foto_pk)
            categorias =  foto.categorias.all()
        queryset = Fotografia.objects.filter(publica=True, aprobada=True, estatus=True, categorias__in=categorias)
        print(queryset.query)
        return queryset

class ListMisFotos(ListAPIView):
    permission_classes = (IsAuthenticated, FotopartnerPermission)
    authentication_classes = (SessionAuthentication,)
    serializer_class = FotografiaSerializer

    def get_queryset(self):
        queryset = Fotografia.objects.filter(usuario=self.request.user).order_by('-fecha_alta')
        return queryset
