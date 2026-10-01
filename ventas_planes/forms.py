from django import forms
from django.db.models import Q
from django.utils import timezone
from .models import VentaPlan

class VentaPlanForm(forms.ModelForm):
    class Meta:
        model = VentaPlan
        fields = ['cliente', 'plan', 'fecha_inicio']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        hoy = timezone.now().date()
        self.fields['plan'].queryset = self.fields['plan'].queryset.filter(
            Q(tipo_plan='estandar') |
            Q(tipo_plan='promocion', fecha_inicio_promocion__lte=hoy, fecha_fin_promocion__gte=hoy)
        )