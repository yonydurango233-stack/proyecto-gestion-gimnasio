from django.urls import path
from . import views

urlpatterns = [
    path('registrar/', views.registrar_venta_plan, name='registrar_venta_plan'),
    path('ultimo-plan/<int:cliente_id>/', views.ultimo_plan_cliente, name='ultimo_plan_cliente'),
]