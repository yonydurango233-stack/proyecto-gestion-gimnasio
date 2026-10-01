from django.urls import path
from . import views

urlpatterns = [
    path('registrar/', views.registrar_venta_producto, name='registrar_venta_producto'),
]