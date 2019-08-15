import conekta
from django.http import JsonResponse

from config.models import Usuario, Tarjeta
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