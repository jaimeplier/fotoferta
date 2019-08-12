from rest_framework.generics import ListAPIView

from config.models import Categoria, Etiqueta
from webservices.serializers import CategoriasSerializer, EtiquetaSerializer


class ListCategorias(ListAPIView):

    serializer_class = CategoriasSerializer

    def get_queryset(self):
        queryset = Categoria.objects.filter(estatus=True).order_by('nombre')
        return queryset

class ListEtiquetas(ListAPIView):

    serializer_class = EtiquetaSerializer

    def get_queryset(self):
        queryset = Etiqueta.objects.filter(estatus=True).order_by('nombre')
        return queryset