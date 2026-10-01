from django.db import models
from django.utils import timezone

class Plan(models.Model):
    TIPO_PLAN_CHOICES = [
        ('estandar', 'Estándar'),
        ('promocion', 'Promoción'),
    ]
    UNIDAD_DURACION_CHOICES = [
        ('dias', 'Días'),
        ('meses', 'Meses'),
    ]

    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    tipo_plan = models.CharField(max_length=20, choices=TIPO_PLAN_CHOICES, default='estandar')
    unidad_duracion = models.CharField(max_length=10, choices=UNIDAD_DURACION_CHOICES, default='meses')
    duracion = models.IntegerField()
    fecha_inicio_promocion = models.DateField(null=True, blank=True)
    fecha_fin_promocion = models.DateField(null=True, blank=True)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Plan"
        verbose_name_plural = "Planes"

    def esta_vigente(self):
        if self.tipo_plan == 'promocion':
            hoy = timezone.now().date()
            if self.fecha_inicio_promocion and self.fecha_fin_promocion:
                return self.fecha_inicio_promocion <= hoy <= self.fecha_fin_promocion
            return False
        return self.activo

    def __str__(self):
        return f"{self.nombre} - ${self.precio}"