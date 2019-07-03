from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from config.models import Marco
from webservices.serializers import EstatusSerializer


class CambiarEstatusMarco(APIView):
    authentication_classes = (SessionAuthentication, )
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = EstatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            admin_ciudad = Marco.objects.get(pk=serializer.validated_data.get('pk'))
            if admin_ciudad.estatus:
                admin_ciudad.estatus = False
            else:
                admin_ciudad.estatus = True
            admin_ciudad.save()
        except:
            return Response({'Error': 'Objeto no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'result': 1}, status=status.HTTP_200_OK)

    def get_serializer(self):
        return EstatusSerializer()