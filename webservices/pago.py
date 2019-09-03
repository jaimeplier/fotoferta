import jwt
from django.db.models import F
from django.template.loader import get_template
from django.utils import timezone
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from config.conekta import crear_orden_tarjeta, crear_cliente, crear_orden_oxxo, crear_orden_spei
from config.models import Direccion, Tarjeta, Orden, FormaPago, Producto, EstatusCompra, EstatusPago, Descarga, Usuario, \
    Fotografia
from fotofertas.settings import KEY_FOTO
from webapp.mail import sendMail
from webservices.Permissions import FotopartnerPermission
from webservices.serializers import DireccionSerializer, TarjetaSerializer, PagarOrdenSerializer


class ListDirecciones(ListAPIView):
    permission_classes = (IsAuthenticated, FotopartnerPermission)
    authentication_classes = (SessionAuthentication,)

    serializer_class = DireccionSerializer

    def get_queryset(self):
        queryset = Direccion.objects.filter(usuario=self.request.user, estatus=True)
        return queryset

class ListTarjetas(ListAPIView):
    permission_classes = (IsAuthenticated, FotopartnerPermission)
    authentication_classes = (SessionAuthentication,)

    serializer_class = TarjetaSerializer

    def get_queryset(self):
        queryset = Tarjeta.objects.filter(usuario=self.request.user, estatus=True)
        return queryset

class PagarOrden(APIView):
    permission_classes = (IsAuthenticated, FotopartnerPermission)
    authentication_classes = (SessionAuthentication,)

    def post(self, request):
        serializer = PagarOrdenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # cliente = Fotografo.objects.get(pk=request.user.pk)

        # ---> OBTENER Datos <---

        orden = Orden.objects.filter(usuario=self.request.user, estatus_compra__pk=1, estatus__pk=1).first()
        metodo_pago = FormaPago.objects.get(pk=serializer.validated_data['metodo_pago'])
        direccion = Direccion.objects.filter(pk=serializer.data['direccion']).first()
        tarjeta = Tarjeta.objects.filter(pk=serializer.data['tarjeta']).first()
        try:
            o = Orden.objects.get(usuario=self.request.user, estatus_compra__pk=1, estatus__pk=1)
            num_productos_fisicos = Producto.objects.filter(usuario=self.request.user, orden = orden, tipo_compra__pk=2).count()
            total_productos = Producto.objects.filter(usuario=self.request.user, orden = orden).count()
        except Orden.DoesNotExist:
            return Response({'error': 'El carrito esta vacío'}, status=status.HTTP_404_NOT_FOUND)

        if total_productos == 0:  # Carrito vacio
            return Response({'error': 'El carrito esta vacío'}, status=status.HTTP_403_FORBIDDEN)
        if num_productos_fisicos == 0 and orden.total==0:  # Compra de productos digitales gratuitos
            return Response({'error': 'No es posible comprar fotos gratuitas'}, status=status.HTTP_403_FORBIDDEN)
        # validaciones para direccion
        if num_productos_fisicos == 0: # Orden de productos digitales
            # Si proporcionó una dirección
            if direccion is not None:
                orden.direccion = direccion
                orden.save()
            # Sino asignar direccion generica para generar orden en conekta
            else:
                u = Usuario.objects.get(correo='admin@fotofertas.com')
                dir_gen = Direccion.objects.filter(usuario=u).first()
                orden.direccion = dir_gen
                orden.save()
        else: # Si la orden tiene productos fisicos, ver si proporcionó dirección
            if direccion is not None:
                orden.direccion = direccion
                orden.save()
            else:
                return Response({'error': 'Se requiere una dirección'}, status=status.HTTP_400_BAD_REQUEST)

        if orden.usuario.customer_id is None:
            customer_id = crear_cliente(request)
            if type(customer_id) is int:
                return Response({'error': 'Ocurrió un error al procesar la orden'},
                                status=status.HTTP_412_PRECONDITION_FAILED)
        orden.forma_pago = metodo_pago
        orden.save()
        # Verificar metodos de pago
        if metodo_pago.nombre == 'Tarjeta':
            if tarjeta is not None:
                tarjeta = Tarjeta.objects.get(pk=serializer.validated_data['tarjeta'])
                token_tarjeta = tarjeta.token
            else:
                return Response({'error': 'No se encontró la tarjeta'}, status=status.HTTP_404_NOT_FOUND)

            order_conekta = crear_orden_tarjeta(request, orden, token_tarjeta)
            if type(order_conekta) is str:
                return Response({'error': order_conekta},
                                status=status.HTTP_412_PRECONDITION_FAILED)
            estatus_pago = EstatusPago.objects.get(pk=2) # Pagado
            orden.estatus_pago = estatus_pago
            orden.fecha_compra = timezone.now()
            orden.save()
            productos = Producto.objects.filter(orden=orden)
            list_fotos =productos.values_list('foto__pk', flat=True)
            fotos = Fotografia.objects.filter(pk__in=list_fotos)
            fotos.update(num_compras=F('num_compras')+1)
            productos.update(estatus_pago=estatus_pago)
            productos.filter(subtotal__gt=0)
            descargas = []
            for producto in productos:
                encoded = jwt.encode({'producto': producto.pk, 'foto': producto.foto.pk, 'usuario': self.request.user.pk}, KEY_FOTO, algorithm='HS256')
                token = encoded.decode('UTF-8')
                descargas.append(Descarga.objects.create(producto=producto, orden=orden, usuario=self.request.user, token=token))

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

        elif metodo_pago.nombre == 'Oxxo':
            order_conekta = crear_orden_oxxo(request, orden)
            if type(order_conekta) is str:
                return Response({'error': order_conekta},
                                status=status.HTTP_412_PRECONDITION_FAILED)
        elif metodo_pago.nombre == 'Spei':
            order_conekta = crear_orden_spei(request, orden)
            if type(order_conekta) is str:
                return Response({'error': order_conekta},
                                status=status.HTTP_412_PRECONDITION_FAILED)


        return Response({'exito': 'Orden generada correctamente'}, status=status.HTTP_200_OK)


    def get_serializer(self):
        return PagarOrdenSerializer()