from django.forms import ModelForm, Select, BooleanField

from config.models import CodigoMarco


class CodigoMarcoForm(ModelForm):
    class Meta:
        model = CodigoMarco
        estatus = BooleanField(required=False)
        fields = ['codigo',
                  'estatus'
                  ]
        labels = {'codigo': 'Código',

                  }


        # widgets = { 'estatus': Select(choices=[[True, 'Activo'], [False, 'Inactivo']])}