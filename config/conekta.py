import conekta
from django.http import JsonResponse

from config.models import Usuario, Tarjeta, Orden, Producto
from fotofertas.settings import CONEKTA_PRIVATE_KEY, CONEKTA_LOCALE, CONEKTA_VERSION, CONEKTA_PUBLIC_KEY
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
        orden.save()
    except conekta.ConektaError as e:
        return str(e.error_json['details'][0]['message'])
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
