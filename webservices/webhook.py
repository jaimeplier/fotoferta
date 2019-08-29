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
        print('Funciona')
        print(request)
        print(request.data)
        print(request['object'])
        type = request['type']
        if type == 'order.paid':
            print('orden pagado')
            print(request.data)
            return HttpResponse(status=200)
            id = request.data['data']['object']['order_id']
            try:
                p = Orden.objects.get(order_id=id)
                p.estatus_pago = EstatusPago(pk=2)
                p.save()
            except Orden.DoesNotExist:
                pass
        return Response({'received data': request.data})
        obj = request.data['object']
