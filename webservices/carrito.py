from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from config.models import Fotografia, Fotografo, Orden, EstatusCompra, EstatusPago, Producto, TipoCompra
from webservices.Permissions import FotopartnerPermission
from webservices.serializers import AddFotoCarritoSerializer, ProductoSerializer, ProductoPKSerializer

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
        actualizar_costo_producto_orden(producto, orden_carrito.first())


        return Response({'exito': 'producto agregado a carrito exitosamente'}, status=status.HTTP_200_OK)


    def get_serializer(self):
        return AddFotoCarritoSerializer()

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
        producto.delete()

        return Response({'exito': 'Producto eliminado del carrito exitosamente'}, status=status.HTTP_200_OK)

    def get_serializer(self):
        return ProductoPKSerializer()

def actualizar_costo_envio(orden):
    productos = Producto.objects.filter(orden=orden)
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


def actualizar_costo_producto_orden(producto, orden):
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
    return