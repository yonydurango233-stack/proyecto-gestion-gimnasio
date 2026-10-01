from django import forms
from .models import Egreso

class EgresoForm(forms.ModelForm):
    class Meta:
        model = Egreso
        fields = ['concepto', 'monto', 'fecha', 'metodo_pago']