from django.db import models

class Producto(models.Model):
    CATEGORIAS = [
        ('hidratacion', 'Hidratación'),
        ('suplementos', 'Suplementos'),
        ('ropa', 'Ropa'),
        ('accesorios', 'Accesorios'),
    ]

    nombre = models.CharField(max_length=100)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    activo = models.BooleanField(default=True)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        return f"{self.nombre} - Stock: {self.stock}"