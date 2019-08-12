from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from config.models import Direccion, Tarjeta, Orden, FormaPago
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

        orden = Orden.objects.get(pk=serializer.validated_data['orden'])
        metodo_pago = FormaPago.objects.get(pk=serializer.validated_data['metodo_pago'])
        direccion = Direccion.objects.get(pk=serializer.validated_data['direccion'])
        tarjeta = None
        if metodo_pago.nombre == 'Tarjeta':
            tarjeta = Tarjeta.objects.get(pk=serializer.validated_data['tarjeta'])



        return Response({'exito': 'producto agregado a carrito exitosamente'}, status=status.HTTP_200_OK)


    def get_serializer(self):
        return AddFotoCarritoSerializer()