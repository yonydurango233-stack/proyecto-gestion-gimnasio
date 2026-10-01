from django.urls import path
from . import views

urlpatterns = [
    path('registrar/', views.registrar_egreso, name='registrar_egreso'),
]