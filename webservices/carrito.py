from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from config.models import Fotografia, Fotografo, Orden, EstatusCompra, EstatusPago, Producto, TipoCompra, Marco, \
    PapelImpresion, FotoPrecio, Tamanio, Textura
from webservices.Permissions import FotopartnerPermission
from webservices.serializers import AddFotoCarritoSerializer, ProductoSerializer, ProductoPKSerializer, \
    EditProductoSerializer, MarcoSerializer, TamanioSerializer, PapelImpresionSerializer, TexturaSerializer, \
    FotoPrecioSerializer


class AgregarCarrrito(APIView):
    permission_classes = (IsAuthenticated, FotopartnerPermission)
    authentication_classes = (SessionAuthentication,)

    def post(self, request):
        serializer = AddFotoCarritoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # cliente = Fotografo.objects.get(pk=request.user.pk)

        # ---> OBTENER FOTOGRAFIA <---

        foto = Fotografia.objects.get(pk=serializer.validated_data['pk'])

        # ---> Buscar orden en estatus de carrito o crearla <---

        orden_carrito = Orden.objects.filter(usuario=request.user, estatus_compra__pk=1)
        if len(orden_carrito) == 0:
            estatus_compra = EstatusCompra.objects.get(pk=1) # estatus de carrito
            estatus_pago = EstatusPago.objects.get(pk=1) # estatus orden no pagada
            orden_carrito = Orden.objects.create(usuario=request.user, estatus=estatus_pago,
                                                 estatus_compra=estatus_compra)

        # ---> Agregar producto a la orden de compra con estatus de carrito <---
        tipo_compra = TipoCompra.objects.get(pk=serializer.validated_data['tipo_compra'])
        producto = Producto.objects.create(usuario=request.user, foto=foto, orden=orden_carrito.first(), tipo_compra=tipo_compra)

        actualizar_costo_envio(orden_carrito.first())
        actualizar_costo_producto_orden(producto, orden_carrito.first(), 'add')


        return Response({'exito': 'producto agregado a carrito exitosamente', 'producto_pk':producto.pk}, status=status.HTTP_200_OK)


    def get_serializer(self):
        return AddFotoCarritoSerializer()


class ModificarProductoCarrito(APIView):
    permission_classes = (IsAuthenticated, FotopartnerPermission)
    authentication_classes = (SessionAuthentication,)

    def post(self, request):
        serializer = EditProductoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # ---> OBTENER Producto <---
        producto = Producto.objects.select_for_update().get(pk=serializer.validated_data['producto'])
        marco = Marco.objects.get(pk=serializer.validated_data['marco'])
        papel = PapelImpresion.objects.get(pk=serializer.validated_data['papel_impresion'])
        maria_luisa = PapelImpresion.objects.filter(pk=serializer.data['maria_luisa']).first()
        tipo_compra = TipoCompra.objects.get(pk=2)

        producto.marco = marco
        producto.papel_impresion = papel
        producto.maria_luisa = maria_luisa
        producto.tipo_compra = tipo_compra
        producto.save()

        actualizar_costo_envio(producto)

        # Actualiza costos de la orden
        orden=Orden.objects.get(pk=producto.orden.pk)
        actualizar_costo_producto_orden(producto, orden, 'delete')
        actualizar_costo_producto_orden(producto, orden, 'add')


        return Response({'exito': 'producto modificado exitosamente'}, status=status.HTTP_200_OK)


    def get_serializer(self):
        return EditProductoSerializer()

class ListCarrito(ListAPIView):
    permission_classes = (IsAuthenticated, FotopartnerPermission)
    authentication_classes = (SessionAuthentication,)

    serializer_class = ProductoSerializer

    def get_queryset(self):
        queryset = Producto.objects.filter(usuario=self.request.user, orden__estatus_compra__pk=1)
        return queryset

class DeleteCarrito(APIView):
    permission_classes = (IsAuthenticated, FotopartnerPermission)
    authentication_classes = (SessionAuthentication,)

    def post(self, request):
        serializer = ProductoPKSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # ---> OBTENER FOTOGRAFIA <---

        producto = Producto.objects.filter(pk=serializer.validated_data['pk'], usuario=request.user)
        orden_pk = producto.first().orden.pk
        actualizar_costo_producto_orden(producto.first(), producto.first().orden, 'delete')
        producto.delete()
        orden = Orden.objects.get(pk=orden_pk)
        actualizar_costo_envio(orden)
        return Response({'exito': 'Producto eliminado del carrito exitosamente'}, status=status.HTTP_200_OK)

    def get_serializer(self):
        return ProductoPKSerializer()

class ListMarco(ListAPIView):
    """
        **Parámetros**

        1. producto: número entero del ID del producto
        2. tamanio: número entero del ID del tamaño del marco deseado

        """
    permission_classes = (IsAuthenticated, FotopartnerPermission)
    authentication_classes = (SessionAuthentication,)

    serializer_class = MarcoSerializer

    def get_queryset(self):
        producto_pk = self.request.query_params.get('producto', None)
        tamanio_pk = self.request.query_params.get('tamanio', None)
        queryset = Marco.objects.none()
        if producto_pk is not None:
            try:
                producto = Producto.objects.get(pk=producto_pk)
            except:
                raise ValidationError({"error": ["No existe el producto"]})
            try:
                tamanio = Tamanio.objects.get(pk=tamanio_pk)
            except:
                raise ValidationError({"error": ["No existe el tamaño seleccionado"]})

            tamanio_foto_precio = FotoPrecio.objects.get(tamanio=producto.foto.tamanio, tipo_foto=producto.foto.tipo_foto)
            area = tamanio_foto_precio.min_area
            tamanios = FotoPrecio.objects.filter(min_area__gte=area).values_list('tamanio__pk', flat=True)
            if producto.foto.tamanio.pk not in tamanios:
                raise ValidationError({"error": ["El tamaño no es elegible para este producto"]})
            queryset = Marco.objects.filter(tamanio__pk=tamanio.pk, estatus=True)
        return queryset

class ListTamanio(ListAPIView):
    """
        **Parámetros**

        1. producto: número entero del ID del producto

        """
    permission_classes = (IsAuthenticated, FotopartnerPermission)
    authentication_classes = (SessionAuthentication,)

    serializer_class = FotoPrecioSerializer
    def get_queryset(self):
        producto_pk = self.request.query_params.get('producto', None)
        queryset = FotoPrecio.objects.none()
        if producto_pk is not None:
            try:
                producto = Producto.objects.get(pk=producto_pk)
            except:
                raise ValidationError({"error": ["No existe el producto seleccionado"]})
            tamanio_foto_precio = FotoPrecio.objects.get(tamanio=producto.foto.tamanio, tipo_foto=producto.foto.tipo_foto)
            area = tamanio_foto_precio.min_area
            queryset = FotoPrecio.objects.filter(min_area__lte=area)
            #queryset = Tamanio.objects.filter(pk__in=tamanios)
        return queryset

class ListTipoPapel(ListAPIView):
    """
        **Parámetros**

        1. tamanio: número entero del ID del tamaño de papel

        """
    permission_classes = (IsAuthenticated, FotopartnerPermission)
    authentication_classes = (SessionAuthentication,)

    serializer_class = PapelImpresionSerializer

    def get_queryset(self):
        tamanio_pk = self.request.query_params.get('tamanio', None)
        queryset = PapelImpresion.objects.none()
        if tamanio_pk is not None:
            try:
                tamanio = Tamanio.objects.get(pk=tamanio_pk)
            except:
                raise ValidationError({"error": ["No existe el tamaño seleccionado"]})
            queryset = PapelImpresion.objects.filter(tamanio=tamanio, estatus=True)
        return queryset


class ListTexturas(ListAPIView):
    """
        **Descripción**

        Lista todos los lienzos o texturas para el simulador de marcos

        """
    permission_classes = (IsAuthenticated, FotopartnerPermission)
    authentication_classes = (SessionAuthentication,)

    serializer_class = TexturaSerializer

    def get_queryset(self):
        queryset = Textura.objects.filter(estatus=True)
        return queryset


def actualizar_costo_envio(orden):
    productos = Producto.objects.filter(orden=orden, tipo_compra__pk=2)
    cantidad_productos = len(productos)

    orden.total -= orden.costo_envio
    orden.costo_envio = 0

    if cantidad_productos == 0 or cantidad_productos >= 5:  # Envío gratuito
        orden.costo_envio = 0
    elif cantidad_productos >= 1 and cantidad_productos <= 3:
        orden.costo_envio = 99
    elif cantidad_productos == 4:
        orden.costo_envio = 198
    orden.total += orden.costo_envio
    orden.save()
    return


def actualizar_costo_producto_orden(producto, orden, accion):
    if accion == 'add':
        if producto.tipo_compra.pk == 1:  # Compra digital
            producto.subtotal = producto.foto.precio
        else:  # Compra Fisica
            producto.subtotal += producto.foto.precio
            if producto.marco:
                producto.subtotal += producto.marco.precio
            if producto.maria_luisa:
                producto.subtotal += producto.maria_luisa.precio
            if producto.papel_impresion:
                producto.subtotal += producto.papel_impresion.precio
        producto.save()
        orden.total += producto.subtotal
        orden.save()
    elif accion == 'delete':
        orden.total -= producto.subtotal
        orden.save()
    return