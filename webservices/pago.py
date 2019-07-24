from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from config.models import Direccion, Tarjeta
from webservices.Permissions import FotopartnerPermission
from webservices.serializers import DireccionSerializer, TarjetaSerializer


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