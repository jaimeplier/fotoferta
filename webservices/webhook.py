import jwt
from django.db.models import F
from django.http import HttpResponse
from django.template.loader import get_template
from django.utils import timezone
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from config.models import Orden, EstatusPago, Producto, Descarga, Fotografia
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
            try:
                orden = Orden.objects.get(order_id=id)
                estatus_pago = EstatusPago.objects.get(pk=2)  # Pagado
                orden.estatus = estatus_pago
                orden.fecha_compra = timezone.now()
                orden.save()
                productos = Producto.objects.filter(orden=orden)
                list_fotos = productos.values_list('foto__pk', flat=True)
                fotos = Fotografia.objects.filter(pk__in=list_fotos)
                fotos.update(num_compras=F('num_compras') + 1)
                productos.update(estatus_pago=estatus_pago)
                productos.filter(subtotal__gt=0)
                descargas = []
                for producto in productos:
                    encoded = jwt.encode(
                        {'producto': producto.pk, 'foto': producto.foto.pk, 'usuario': orden.usuario.pk}, KEY_FOTO,
                        algorithm='HS256')
                    token = encoded.decode('UTF-8')
                    descargas.append(
                        Descarga.objects.create(producto=producto, orden=orden, usuario=orden.usuario, token=token))

                email_template_name = 'mailing/descargas.html'
                subject = "Productos Digitales"
                to = [orden.usuario.correo]
                ctx = {
                    'productos': descargas,
                    'request': request,
                    'user': orden.usuario,
                    'orden': orden
                }
                message = get_template(email_template_name).render(ctx)
                sendMail(to, subject, message)
            except Orden.DoesNotExist:
                pass
        obj = request.data['object']
        return Response({'received data': request.data})
