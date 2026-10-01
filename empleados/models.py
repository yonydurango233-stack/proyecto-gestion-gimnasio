from django.db import models

from django.db import models
from django.contrib.auth.models import User

class Empleado(models.Model):
    ROLES = [
        ('entrenador', 'Entrenador'),
        ('recepcionista', 'Recepcionista'),
        ('administrador', 'Administrador'),
    ]

    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=20, blank=True)
    rol = models.CharField(max_length=20, choices=ROLES)
    fecha_ingreso = models.DateField()
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Empleado"
        verbose_name_plural = "Empleados"

    def __str__(self):
        return f"{self.usuario.get_full_name()} - {self.rol}"
