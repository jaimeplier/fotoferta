from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from config.models import Contactanos
from webservices.serializers import ContactanosSerializer


class ListContactanos(ListAPIView):

    serializer_class = ContactanosSerializer

    def get_queryset(self):
        queryset = Contactanos.objects.all()
        return queryset