from django.db import models
from django.utils import timezone
from empleados.models import Empleado

class Egreso(models.Model):
    METODOS_PAGO = [
    ('efectivo', 'Efectivo'),
    ('transferencia', 'Transferencia'),
]

    concepto = models.CharField(max_length=100)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField(default=timezone.now)
    empleado = models.ForeignKey(Empleado, on_delete=models.PROTECT)
    metodo_pago = models.CharField(max_length=20, choices=METODOS_PAGO)

    def __str__(self):
        return f"{self.concepto} - ${self.monto} ({self.fecha})"