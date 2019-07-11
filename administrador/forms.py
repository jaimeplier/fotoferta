from django.forms import ModelForm, Select, BooleanField, PasswordInput

from config.models import CodigoMarco, Tamanio, Marco, MariaLuisa, ModeloMariaLuisa, PersonalAdministrativo, \
    Textura, Logo, MenuFotopartner, Promocion, TipoPapel, PapelImpresion


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

class PapelImpresionForm(ModelForm):
    class Meta:
        model = PapelImpresion

        fields = [
            'tipo_papel',
            'tamanio',
            'precio',
            'estatus',
        ]

        labels = {
            'tamanio': 'Tamaño',
            'tipo_papel': 'Tipo de papel',
              }

class TipoPapelForm(ModelForm):
    class Meta:
        model = TipoPapel

        fields = [
            'nombre',
            'estatus'
        ]

class TexturaForm(ModelForm):
    class Meta:
        model = Textura

        fields = [
            'nombre',
            'imagen',
        ]

class LogoForm(ModelForm):
    class Meta:
        model = Logo

        fields = [
            'nombre', 'imagen',
        ]

class MenuFotopartnerForm(ModelForm):
    class Meta:
        model = MenuFotopartner

        fields = ['nombre']


class PersonalAdministrativoForm(ModelForm):
    class Meta:
        model = PersonalAdministrativo

        fields = ['nombre',
                  'correo',
                  'password',
                  'estatus'
                  ]
        widgets = {'password': PasswordInput()}


class PromocionForm(ModelForm):
    class Meta:
        model = Promocion
        fields = [
                  'nombre',
                  'total_cupones',
                  'usos_por_usuario',
                  'codigo_promocion',
                  'fecha_inicio',
                  'fecha_fin',
                  'tipo_promocion',
                  'porcentaje_cantidad',
                  'tipo_compra',
                  'imagen',
                  'forma_pago',
                  'estatus',
                  ]

        labels = {'nombre': 'Nombre',
                  }


