from django import forms
from .models import EntradaDiaria, TipoEntrada
from clientes.models import Cliente

class EntradaDiariaForm(forms.ModelForm):
    class Meta:
        model = EntradaDiaria
        fields = ['cliente', 'tipo_entrada']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        predeterminado = TipoEntrada.objects.filter(predeterminado=True, activo=True).first()
        if predeterminado:
            self.fields['tipo_entrada'].initial = predeterminado.id

        clientes_varios = Cliente.objects.filter(numero_documento='00000000').first()
        if clientes_varios:
            self.fields['cliente'].initial = clientes_varios.id