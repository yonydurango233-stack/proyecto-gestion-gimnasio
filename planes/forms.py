from django import forms
from .models import Plan


class PlanForm(forms.ModelForm):
    class Meta:
        model = Plan
        fields = [
            'nombre',
            'precio',
            'tipo_plan',
            'unidad_duracion',
            'duracion',
            'fecha_inicio_promocion',
            'fecha_fin_promocion',
            'descripcion',
            'activo',
        ]
        widgets = {
            'fecha_inicio_promocion': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'fecha_fin_promocion': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }