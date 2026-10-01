from django.db import models
from clientes.models import Cliente
from productos.models import Producto
from empleados.models import Empleado


class Venta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    empleado = models.ForeignKey(Empleado, on_delete=models.PROTECT)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"

    def __str__(self):
        return f"Venta #{self.id} - {self.cliente} ({self.fecha})"


class VentaProducto(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.IntegerField(default=1)
    precio_pagado = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Producto de la Venta"
        verbose_name_plural = "Productos de la Venta"

    def __str__(self):
        return f"{self.producto} x{self.cantidad}"


class Pago(models.Model):
    METODOS_PAGO = [
        ('efectivo', 'Efectivo'),
        ('transferencia', 'Transferencia'),
    ]

    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='pagos')
    metodo_pago = models.CharField(max_length=20, choices=METODOS_PAGO)
    monto = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"

    def __str__(self):
        return f"{self.metodo_pago} - ${self.monto}"