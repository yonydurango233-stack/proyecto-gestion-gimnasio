from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from empleados.models import Empleado
from .forms import EgresoForm

@login_required
def registrar_egreso(request):
    if request.method == 'POST':
        form = EgresoForm(request.POST)
        if form.is_valid():
            egreso = form.save(commit=False)

            # empleado autocompletado según el usuario logueado
            egreso.empleado = Empleado.objects.get(usuario=request.user)

            egreso.save()
            messages.success(request, f'Egreso registrado: {egreso.concepto} - ${egreso.monto}')
            return redirect('inicio')
    else:
        form = EgresoForm()

    return render(request, 'egresos/registrar_egreso.html', {'form': form})