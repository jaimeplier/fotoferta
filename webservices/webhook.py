from django.http import HttpResponse
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from config.models import Orden, EstatusPago
from webservices.Permissions import WebHookPermission


class WebHook(APIView):
    permission_classes = (AllowAny, WebHookPermission)
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    parser_classes = (JSONParser,)

    def post(self, request):
        type = request['type']
        if type == 'order.paid':
            id = request.data['data']['object']['order_id']
            try:
                p = Orden.objects.get(order_id=id)
                p.estatus_pago = EstatusPago(pk=2)
                p.save()
            except Orden.DoesNotExist:
                pass
        obj = request.data['object']
        return Response({'received data': request.data})
