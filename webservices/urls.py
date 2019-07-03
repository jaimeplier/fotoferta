from django.urls import path

from webservices.views import CambiarEstatusMarco

app_name = 'webservices'



urlpatterns = [
    path('enviarCodigo/', CambiarEstatusMarco.as_view(), name='enviar_codigo'),

]
