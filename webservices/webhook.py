import jwt
from django.http import HttpResponse
from django.template.loader import get_template
from django.utils import timezone
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from config.models import Orden, EstatusPago, Producto, Descarga
from fotofertas.settings import KEY_FOTO
from webapp.mail import sendMail
from webservices.Permissions import WebHookPermission


class WebHook(APIView):
    permission_classes = (AllowAny, WebHookPermission)
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    parser_classes = (JSONParser,)

    def post(self, request):
        type = request.data['type']
        if type == 'order.paid':
            id = request.data['data']['object']['id']
            print(id)
            try:
                orden = Orden.objects.get(order_id=id)
                estatus_pago = EstatusPago.objects.get(pk=2)  # Pagado
                orden.estatus_pago = estatus_pago
                orden.fecha_compra = timezone.now()
                orden.save()
                print('Orden Guardada')
                productos = Producto.objects.filter(orden=orden)
                productos.update(estatus_pago=estatus_pago)
                productos.filter(subtotal__gt=0)
                print('Productos filtrados')
                descargas = []
                for producto in productos:
                    encoded = jwt.encode(
                        {'producto': producto.pk, 'foto': producto.foto.pk, 'usuario': self.request.user.pk}, KEY_FOTO,
                        algorithm='HS256')
                    token = encoded.decode('UTF-8')
                    descargas.append(
                        Descarga.objects.create(producto=producto, orden=orden, usuario=self.request.user, token=token))
                print(descargas)
                email_template_name = 'mailing/descargas.html'
                subject = "Productos Digitales"
                to = [self.request.user.correo]
                ctx = {
                    'productos': descargas,
                    'request': request,
                    'user': self.request.user,
                    'orden': orden
                }
                message = get_template(email_template_name).render(ctx)
                sendMail(to, subject, message)
                print('Correo enviado')
            except Orden.DoesNotExist:
                pass
        print(request.data['object'])
        obj = request.data['object']
        return Response({'received data': request.data})
