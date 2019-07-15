from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from config.models import Contactanos, Categoria
from webservices.serializers import ContactanosSerializer, CategoriasSerializer


class ListContactanos(ListAPIView):

    serializer_class = ContactanosSerializer

    def get_queryset(self):
        queryset = Contactanos.objects.all()
        return queryset

class ListCategorias(ListAPIView):

    serializer_class = CategoriasSerializer

    def get_queryset(self):
        queryset = Categoria.objects.filter(estatus=True)
        return queryset