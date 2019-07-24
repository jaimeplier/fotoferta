from django.forms import ModelForm

from config.models import Fotografo, Direccion


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