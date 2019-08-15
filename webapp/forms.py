from django.forms import ModelForm, CharField, TextInput

from config.models import Fotografo, Direccion, Tarjeta


class RegistroForm(ModelForm):
    class Meta:
        model = Fotografo

        fields = ['nombre',
                  'correo',
                  'password',
                  'terminos_condiciones'
                  ]

class DireccionForm(ModelForm):
    class Meta:
        model = Direccion
        fields = [
                  'calle',
                  'num_exterior',
                  'num_interior',
                  'referencias',
                  ]


        labels = {
            'calle': 'Calle',
            'num_exterior': 'Num. Exterior',
            'num_interior': 'Num. Interior',
            'referencias': 'Referencias'
                  }


class TarjetaForm(ModelForm):
    numero = CharField(label='Número de la tarjeta de crédito o débito', max_length=20)
    numero.widget.attrs["data-conekta"] = "card[number]"
    CVC = CharField(label='CVC', max_length=4)
    CVC.widget.attrs["data-conekta"] = "card[cvc]"
    expiracion_mes = CharField(label='Mes de expiración (MM)', max_length=2)
    expiracion_mes.widget.attrs["data-conekta"] = "card[exp_month]"
    expiracion_anio = CharField(label='Año de expiración (AAAA)', max_length=4)
    expiracion_anio.widget.attrs["data-conekta"] = "card[exp_year]"
    token = CharField(max_length=100)


    class Meta:
        model=Tarjeta
        fields=[
            'nombre_propietario',
            'alias'
        ]
        labels = {
            'nombre_propietario': 'Nombre que aparece en la tarjeta',
            'alias': 'Nombre con el que identificarás tu tarjeta (alias)'
        }
        widgets = {
            'nombre_propietario': TextInput(attrs={'data-conekta': 'card[name]'}),
        }

class TarjetaEditForm(ModelForm):
    expiracion_mes = CharField(label='Mes de expiración (MM)', max_length=2)
    expiracion_mes.widget.attrs["data-conekta"] = "card[exp_month]"
    expiracion_anio = CharField(label='Año de expiración (AAAA)', max_length=4)
    expiracion_anio.widget.attrs["data-conekta"] = "card[exp_year]"


    class Meta:
        model=Tarjeta
        fields=[
            'nombre_propietario',
            'alias'
        ]
        labels = {
            'nombre_propietario': 'Nombre que aparece en la tarjeta',
            'alias': 'Nombre con el que identificarás tu tarjeta (alias)'
        }
        widgets = {
            'nombre_propietario': TextInput(attrs={'data-conekta': 'card[name]'}),
        }