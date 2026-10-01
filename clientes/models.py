from django.db import models

class Cliente(models.Model):
    numero_documento = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    correo = models.EmailField(blank=True)
    fecha_nacimiento = models.DateField()
    fecha_inscripcion = models.DateField()
    foto = models.ImageField(upload_to='clientes_fotos/', blank=True, null=True)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.numero_documento}"