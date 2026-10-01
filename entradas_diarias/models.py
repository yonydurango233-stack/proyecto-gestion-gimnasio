from django.db import models
from clientes.models import Cliente
from empleados.models import Empleado

class TipoEntrada(models.Model):
    nombre = models.CharField(max_length=50)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    activo = models.BooleanField(default=True)
    predeterminado = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Tipo de Entrada"
        verbose_name_plural = "Tipos de Entrada"

    def __str__(self):
        return self.nombre


class EntradaDiaria(models.Model):
    METODOS_PAGO = [
        ('efectivo', 'Efectivo'),
        ('transferencia', 'Transferencia'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    empleado = models.ForeignKey(Empleado, on_delete=models.PROTECT)
    tipo_entrada = models.ForeignKey(TipoEntrada, on_delete=models.PROTECT)
    fecha = models.DateTimeField(auto_now_add=True)
    precio_pagado = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = models.CharField(max_length=20, choices=METODOS_PAGO)
    metodo_pago_2 = models.CharField(max_length=20, choices=METODOS_PAGO, blank=True, null=True)
    monto_2 = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        verbose_name = "Entrada Diaria"
        verbose_name_plural = "Entradas Diarias"

    def __str__(self):
        return f"{self.cliente} - {self.fecha}"