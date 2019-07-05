from django.forms import ModelForm, Select, BooleanField

from config.models import CodigoMarco, Tamanio, Marco, MariaLuisa, ModeloMariaLuisa, GrosorPapel, TipoPapel, \
        Textura, Logo


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
            'nombre',
            'codigo',
            'tamanio',
            'alto',
            'ancho',
            'grosor_lado',
            'grosor_total',
            'grosor_final',
            'profundidad',
            'peso',
            'precio',
            'imagen_horizontal',
            'imagen_vertical'
        ]

        labels = {
                'nombre': 'Nombre',
                'codigo': 'Código',
                'tamanio': 'Tamaño',
                'alto': 'Alto',
                'ancho': 'Ancho',
                'grosor_lado': 'Grosor lateral',
                'grosor_total': 'Grosor total',
                'grosor_final': 'Grosor final',
                'profundidad': 'Profundidad',
                'peso': 'Peso',
                'precio': 'Precio',
                'imagen_horizontal': 'Imagen horizontal',
                'imagen_vertical': 'Imagen vertical',
              }

class ModeloMarialuisaForm(ModelForm):
    class Meta:
        model = ModeloMariaLuisa
        fields = ['modelo',
                  ]

        labels = {'modelo': 'Modelo',
                  }

class MarialuisaForm(ModelForm):
    class Meta:
        model = MariaLuisa

        fields = [
            'nombre',
            'modelo',
            'precio',
            'tamanio',
            'alto',
            'ancho',
            'imagen',
        ]

        labels = {
            'modelo': 'Modelo',
            'precio': 'Precio',
            'tamanio': 'Tamaño',
            'alto': 'Alto',
            'ancho': 'Ancho',
            'imagen': 'Imagen',
              }

class GrosorPapelForm(ModelForm):
    class Meta:
        model = GrosorPapel

        fields = [
            'medida',
        ]

        labels = {
            'medida': 'Medida',
              }

class TipoPapelForm(ModelForm):
    class Meta:
        model = TipoPapel

        fields = [
            'grosor',
            'precio'
        ]

        labels = {
            'grosor': 'Grosor',
            'precio': 'Precio',
              }

class TexturaForm(ModelForm):
    class Meta:
        model = Textura

        fields = [
            'imagen',
        ]

class LogoForm(ModelForm):
    class Meta:
        model = Logo

        fields = [
            'imagen',
        ]



