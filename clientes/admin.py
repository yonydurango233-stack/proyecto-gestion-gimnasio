from django import forms
from django.contrib import admin
from django.utils import timezone
import datetime
from .models import Cliente


class ClienteAdminForm(forms.ModelForm):
    fecha_nacimiento = forms.DateField(
        widget=forms.SelectDateWidget(
            years=range(timezone.now().year - 90, timezone.now().year - 4)
        ),
        initial=datetime.date(1995, 1, 1),
    )

    class Meta:
        model = Cliente
        fields = '__all__'


class ClienteAdmin(admin.ModelAdmin):
    form = ClienteAdminForm


admin.site.register(Cliente, ClienteAdmin)