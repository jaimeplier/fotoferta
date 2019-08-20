from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from config.conekta import crear_orden_tarjeta, crear_cliente
from config.models import Direccion, Tarjeta, Orden, FormaPago, Producto, EstatusCompra, EstatusPago
from webservices.Permissions import FotopartnerPermission
from webservices.serializers import DireccionSerializer, TarjetaSerializer, PagarOrdenSerializer


class ListDirecciones(ListAPIView):
    permission_classes = (IsAuthenticated, FotopartnerPermission)
    authentication_classes = (SessionAuthentication,)

    serializer_class = DireccionSerializer

    def get_queryset(self):
        queryset = Direccion.objects.filter(usuario=self.request.user, estatus=True)
        return queryset

class ListTarjetas(ListAPIView):
    permission_classes = (IsAuthenticated, FotopartnerPermission)
    authentication_classes = (SessionAuthentication,)

    serializer_class = TarjetaSerializer

    def get_queryset(self):
        queryset = Tarjeta.objects.filter(usuario=self.request.user, estatus=True)
        return queryset

class PagarOrden(APIView):
    permission_classes = (IsAuthenticated, FotopartnerPermission)
    authentication_classes = (SessionAuthentication,)

    def post(self, request):
        serializer = PagarOrdenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # cliente = Fotografo.objects.get(pk=request.user.pk)

        # ---> OBTENER Datos <---

        orden = Orden.objects.filter(usuario=self.request.user, estatus_compra__pk=1, estatus__pk=1).first()
        metodo_pago = FormaPago.objects.get(pk=serializer.validated_data['metodo_pago'])
        direccion = Direccion.objects.filter(pk=serializer.data['direccion']).first()
        tarjeta = Tarjeta.objects.filter(pk=serializer.data['tarjeta']).first()

        if metodo_pago.nombre == 'Tarjeta':
            if tarjeta is not None:
                tarjeta = Tarjeta.objects.get(pk=serializer.validated_data['tarjeta'])
                token_tarjeta = tarjeta.token
            else:
                return Response({'error': 'No se encontró la tarjeta'}, status=status.HTTP_404_NOT_FOUND)
            # Tipo de compra (solo digital o si tiene algun producto fisico)
            num_productos_fisicos = Producto.objects.filter(usuario=self.request.user, orden = orden, tipo_compra__pk=2).count()
            if num_productos_fisicos >0: # Compra con productos fisicos
                if direccion is not None:
                    orden.direccion = direccion
                    orden.save()
                else:
                    return Response({'error': 'Se requiere una dirección'}, status=status.HTTP_400_BAD_REQUEST)
                if orden.usuario.customer_id is None:
                    customer_id = crear_cliente(request)
                    if type(customer_id) is int:
                        return Response({'error': 'Ocurrió un error al procesar la orden'}, status=status.HTTP_412_PRECONDITION_FAILED)

                resultado = crear_orden_tarjeta(request, orden, token_tarjeta)
                if type(resultado) is str:
                    return Response({'error': resultado},
                                    status=status.HTTP_412_PRECONDITION_FAILED)
            estatus_compra = EstatusCompra.objects.get(pk=2) # Ordenado
            estatus_pago = EstatusPago.objects.get(pk=2) # Pagado
            orden.estatus_compra = estatus_compra
            orden.estatus_pago = estatus_pago
            orden.save()
            productos = Producto.objects.filter(orden=orden)
            productos.update(estatus_pago=estatus_pago)


        elif metodo_pago.nombre == 'Oxxo':
            tarjeta = Tarjeta.objects.get(pk=serializer.validated_data['tarjeta'])
        elif metodo_pago.nombre == 'Spei':
            tarjeta = Tarjeta.objects.get(pk=serializer.validated_data['tarjeta'])


        return Response({'exito': 'Orden generada correctamente'}, status=status.HTTP_200_OK)


    def get_serializer(self):
        return PagarOrdenSerializer()