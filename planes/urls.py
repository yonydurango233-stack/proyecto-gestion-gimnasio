from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_planes, name='listar_planes'),
    path('crear/', views.crear_plan, name='crear_plan'),
    path('editar/<int:plan_id>/', views.editar_plan, name='editar_plan'),
]