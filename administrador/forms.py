from django.forms import ModelForm, Select, BooleanField

from config.models import CodigoMarco, Tamanio, Marco


class CodigoMarcoForm(ModelForm):
    class Meta:
        model = CodigoMarco
        estatus = BooleanField(required=False)
        fields = ['codigo',
                  'estatus'
                  ]
        labels = {'codigo': 'Código',
                  }

class TamanioForm(ModelForm):
    class Meta:
        model = Tamanio
        fields = ['nombre',
                  'estatus'
                  ]

        labels = {'nombre': 'Nombre',
                  }


class MarcoForm(ModelForm):
    class Meta:
        model = Marco
        fields = [
            'codigo',
            'tamanio',
            'alto',
            'ancho',
            'profundidad',
            'peso',
            'precio',
        ]

        labels = {'codigo': 'Código',
                'tamanio': 'Tamaño',
                'alto': 'Alto',
                'ancho': 'Ancho',
                'profundidad': 'Profundidad',
                'peso': 'Peso',
                'precio': 'Precio',
                  }


        # widgets = { 'estatus': Select(choices=[[True, 'Activo'], [False, 'Inactivo']])}