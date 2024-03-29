import conekta
from django.http import JsonResponse
from django.template.loader import get_template

from config.models import Usuario, Tarjeta, Orden, Producto, EstatusCompra, EstatusPago
from fotofertas.settings import CONEKTA_PRIVATE_KEY, CONEKTA_LOCALE, CONEKTA_VERSION, CONEKTA_PUBLIC_KEY
from webapp.mail import sendMail

conekta.api_key = "key_eYvWV7gSDkNYXsmr"
conekta.api_version = "2.0.0"

def agregar_tarjeta(request, form=None):
    conekta.api_key = CONEKTA_PRIVATE_KEY
    conekta.locale = CONEKTA_LOCALE
    conekta.api_version = CONEKTA_VERSION
    cliente = Usuario.objects.get(pk=request.user.pk)
    if cliente.customer_id is None:
        try:
            customer = conekta.Customer.create({
                "name": request.POST.get('nombre_propietario'),
                "email": request.user.correo,
                "payment_sources": [{
                    'type': 'card',
                    'token_id': request.POST.get('token')
                }]
            })
            cliente.customer_id = customer.id
            cliente.save()
            source = customer.payment_sources[0]
        except conekta.ConektaError as e:
            return str(e.error_json['details'][0]['message'])
    else:
        try:
            customer = conekta.Customer.find(cliente.customer_id)
            source = customer.createPaymentSource({
                "type": "card",
                "token_id": request.POST.get('token')
            })
        except conekta.ConektaError as e:
            return str(e.error_json['details'][0]['message'])
    return source

def actualizar_tarjeta(request, source_id):
    conekta.api_key = CONEKTA_PRIVATE_KEY
    conekta.locale = CONEKTA_LOCALE
    conekta.api_version = CONEKTA_VERSION
    cliente = Usuario.objects.get(pk=request.user.pk)
    if cliente.customer_id is not None:
        try:
            customer = conekta.Customer.find(cliente.customer_id)
            sources = customer.payment_sources
            source_card = None
            for index, source in enumerate(sources):
                if source.id == source_id:
                    source_card = sources[index]
                    break
            if source_card is None:
                return 'Tarjeta no encontrada'
            source_card.update({"exp_month": request.POST.get('expiracion_mes'),
                                "exp_year": request.POST.get('expiracion_anio'),
                                "name": request.POST.get('nombre_propietario')})
            return 0
        except conekta.ConektaError as e:
            return str(e.error_json['details'][0]['message'])
    else:
        return 'No es posible actualizar los datos de la tarjeta'

def eliminar_tarjeta(request, source_id):
    conekta.api_key = CONEKTA_PRIVATE_KEY
    conekta.locale = CONEKTA_LOCALE
    conekta.api_version = CONEKTA_VERSION
    cliente = Usuario.objects.get(pk=request.user.pk)
    if cliente.customer_id is not None:
        try:
            customer = conekta.Customer.find(cliente.customer_id)
            sources = customer.payment_sources
            source_card = None
            for index, source in enumerate(sources):
                if source.id == source_id:
                    source_card = sources[index]
                    break
            if source_card is None:
                return 'Tarjeta no encontrada'
            source_card.delete()
            return 0
        except conekta.ConektaError as e:
            return str(e.error_json['details'][0]['message'])
    else:
        return 'No es posible actualizar los datos de la tarjeta'

def crear_orden_tarjeta(request, orden, token_card):
    conekta.api_key = CONEKTA_PRIVATE_KEY
    conekta.locale = CONEKTA_LOCALE
    conekta.api_version = CONEKTA_VERSION
    cliente = Usuario.objects.get(pk=request.user.pk)
    productos = Producto.objects.filter(orden=orden)
    costo_envio = int(orden.costo_envio*100)
    paqueteria = "Estafeta"
    line_items = []
    for producto in productos:
        line_items.append({"name": producto.foto.nombre, "unit_price": int(producto.subtotal*100), "quantity": 1})

    if orden.direccion is None:
        address = {
                "street1": 'N/A',
                "city": 'N/A',
                "state": 'N/A',
                "postal_code": 'N/A',
                "country": 'N/A' # shipping_contact - required only for physical goods
        }
    else:
        address = {
                "street1": orden.direccion.direccion_corta(),
                "city": orden.direccion.colonia.municipio.nombre,
                "state": orden.direccion.colonia.municipio.estado.nombre,
                "postal_code": orden.direccion.colonia.cp,
                "country": orden.direccion.colonia.municipio.estado.pais.nombre # shipping_contact - required only for physical goods
        }
    try:
        customer = conekta.Customer.find(cliente.customer_id)
        order = conekta.Order.create({
            "currency": "MXN",
            "shipping_lines": [{
                "amount": costo_envio,
                "carrier": paqueteria
            }],
            "shipping_contact": {
                "address": address
            },
            "customer_info": {
                "customer_id": cliente.customer_id
            },
            "line_items": line_items,
            "charges": [{
                "payment_method": {
                    "type": "default"
                    #"type": "card",
                    #"token_id": token_card
                }
            }]
        })
        orden.order_id = order.id
        estatus_compra = EstatusCompra.objects.get(pk=2)  # Ordenado
        orden.estatus_compra = estatus_compra
        orden.save()
    except conekta.ConektaError as e:
        return str(e.error_json['details'][0]['message'])
    return order

def crear_orden_oxxo(request, orden):
    conekta.api_key = CONEKTA_PRIVATE_KEY
    conekta.locale = CONEKTA_LOCALE
    conekta.api_version = CONEKTA_VERSION
    cliente = Usuario.objects.get(pk=request.user.pk)
    productos = Producto.objects.filter(orden=orden)
    costo_envio = int(orden.costo_envio*100)
    paqueteria = "Estafeta"
    line_items = []
    for producto in productos:
        line_items.append({"name": producto.foto.nombre, "unit_price": int(producto.subtotal*100), "quantity": 1})

    if orden.direccion is None:
        address = {
                "street1": 'N/A',
                "city": 'N/A',
                "state": 'N/A',
                "postal_code": 'N/A',
                "country": 'N/A' # shipping_contact - required only for physical goods
        }
    else:
        address = {
                "street1": orden.direccion.direccion_corta(),
                "city": orden.direccion.colonia.municipio.nombre,
                "state": orden.direccion.colonia.municipio.estado.nombre,
                "postal_code": orden.direccion.colonia.cp,
                "country": orden.direccion.colonia.municipio.estado.pais.nombre # shipping_contact - required only for physical goods
        }
    try:
        customer = conekta.Customer.find(cliente.customer_id)
        order = conekta.Order.create({
            "currency": "MXN",
            "shipping_lines": [{
                "amount": costo_envio,
                "carrier": paqueteria
            }],
            "shipping_contact": {
                "address": address
            },
            "customer_info": {
                "customer_id": cliente.customer_id
            },
            "line_items": line_items,
            "charges": [{
                "payment_method": {
                    "type": "oxxo_cash"
                }
            }]
        })
        orden.order_id = order.id
        estatus_compra = EstatusCompra.objects.get(pk=2)  # Ordenado
        orden.estatus_compra = estatus_compra
        estatus_pago = EstatusPago.objects.get(pk=4)  # Pendiente
        orden.estatus_pago = estatus_pago
        orden.oxxo_order = order.charges[0].payment_method.reference # referencia de Oxxo
        orden.save()
        productos.update(estatus_pago=estatus_pago)
    except conekta.ConektaError as e:
        return str(e.error_json['details'][0]['message'])

    subject = "Pago OXXO Fotofertas"
    to = [orden.usuario.correo]
    ctx = {
        'cantidad_total': (order.amount / 100),
        'request': request,
        'user': orden.usuario,
        'productos': productos,
        'envio': orden.costo_envio,
        'reference': order.charges[0].payment_method.reference,
    }
    message = get_template('mailing/correo_pago_oxxo.html').render(ctx)
    sendMail(to, subject, message)
    return order

def crear_orden_spei(request, orden):
    conekta.api_key = CONEKTA_PRIVATE_KEY
    conekta.locale = CONEKTA_LOCALE
    conekta.api_version = CONEKTA_VERSION
    cliente = Usuario.objects.get(pk=request.user.pk)
    productos = Producto.objects.filter(orden=orden)
    costo_envio = int(orden.costo_envio*100)
    paqueteria = "Estafeta"
    line_items = []
    for producto in productos:
        line_items.append({"name": producto.foto.nombre, "unit_price": int(producto.subtotal*100), "quantity": 1})

    if orden.direccion is None:
        address = {
                "street1": 'N/A',
                "city": 'N/A',
                "state": 'N/A',
                "postal_code": 'N/A',
                "country": 'N/A' # shipping_contact - required only for physical goods
        }
    else:
        address = {
                "street1": orden.direccion.direccion_corta(),
                "city": orden.direccion.colonia.municipio.nombre,
                "state": orden.direccion.colonia.municipio.estado.nombre,
                "postal_code": orden.direccion.colonia.cp,
                "country": orden.direccion.colonia.municipio.estado.pais.nombre # shipping_contact - required only for physical goods
        }
    try:
        customer = conekta.Customer.find(cliente.customer_id)
        order = conekta.Order.create({
            "currency": "MXN",
            "shipping_lines": [{
                "amount": costo_envio,
                "carrier": paqueteria
            }],
            "shipping_contact": {
                "address": address
            },
            "customer_info": {
                "customer_id": cliente.customer_id
            },
            "line_items": line_items,
            "charges": [{
                "payment_method": {
                    "type": "spei"
                }
            }]
        })
        orden.order_id = order.id
        estatus_compra = EstatusCompra.objects.get(pk=2)  # Ordenado
        orden.estatus_compra = estatus_compra
        estatus_pago = EstatusPago.objects.get(pk=4)  # Pendiente
        orden.estatus_pago = estatus_pago
        orden.save()
        productos.update(estatus_pago=estatus_pago)
    except conekta.ConektaError as e:
        return str(e.error_json['details'][0]['message'])

    subject = "Pago SPEI Fotofertas"
    to = [orden.usuario.correo]
    ctx = {
        'cantidad_total': (order.amount / 100),
        'request': request,
        'user': orden.usuario,
        'productos': productos,
        'envio': orden.costo_envio,
        'reference': order.charges[0].payment_method.receiving_account_number,
        'banco': order.charges[0].payment_method.receiving_account_bank,
        'orden_id': orden.pk,
    }
    message = get_template('mailing/correo_pago_spei.html').render(ctx)
    sendMail(to, subject, message)
    return order

def crear_cliente(request):
    conekta.api_key = CONEKTA_PRIVATE_KEY
    conekta.locale = CONEKTA_LOCALE
    conekta.api_version = CONEKTA_VERSION
    cliente = Usuario.objects.get(pk=request.user.pk)
    try:
        customer = conekta.Customer.create({
            "name": cliente.nombre,
            "email": cliente.correo
        })
        cliente.customer_id = customer.id
        cliente.save()
        return  customer.id
    except conekta.ConektaError as e:
        return 1
