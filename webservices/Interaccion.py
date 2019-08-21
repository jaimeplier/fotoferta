from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from config.models import Fotografia, FotoReaccion
from webservices.Permissions import FotopartnerPermission
from webservices.serializers import FotoReaccionSerializer


class ListFavoritos(ListAPIView):
    permission_classes = (IsAuthenticated, FotopartnerPermission)
    authentication_classes = (SessionAuthentication,)

    serializer_class = FotoReaccionSerializer

    def get_queryset(self):
        queryset = FotoReaccion.objects.filter(usuario=self.request.user, reaccion__nombre='Favorito', foto__estatus=True)
        return queryset
