from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('reporte-ventas/', views.reporte_ventas, name='reporte_ventas'),
    path('caja/', views.caja, name='caja'),
    path('ticket/<str:modulo>/<int:id>/', views.ticket_detalle, name='ticket_detalle'),
]