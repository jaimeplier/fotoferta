from django.forms import ModelForm

from config.models import Fotografo


class RegistroForm(ModelForm):
    class Meta:
        model = Fotografo

        fields = ['nombre',
                  'correo',
                  'password',
                  'terminos_condiciones'
                  ]