from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from config.models import Contactanos, Categoria, Colonia, RedSocial
from webservices.serializers import ContactanosSerializer, CategoriasSerializer, ColoniaSerializer, RedSocialSerializer


class ListContactanos(ListAPIView):

    serializer_class = ContactanosSerializer

    def get_queryset(self):
        queryset = Contactanos.objects.all()
        return queryset

class ListDatosCP(ListAPIView):
    """
            **Parámetros**

            1. cp: Código postal a buscar

    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SessionAuthentication, TokenAuthentication)

    serializer_class = ColoniaSerializer

    def get_queryset(self):
        cp = self.request.query_params.get('cp', None)
        queryset = Colonia.objects.none()
        if cp is not None:
            queryset = Colonia.objects.filter(cp=cp)
        return queryset

class ListRedesSociales(ListAPIView):

    serializer_class = RedSocialSerializer

    def get_queryset(self):
        queryset = RedSocial.objects.all()
        return queryset