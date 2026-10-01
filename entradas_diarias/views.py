import json
from decimal import Decimal
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import EntradaDiariaForm
from django.contrib import messages
from .models import TipoEntrada


@login_required
def registrar_entrada(request):
    if request.method == 'POST':
        form = EntradaDiariaForm(request.POST)
        if form.is_valid():
            entrada = form.save(commit=False)
            entrada.empleado = request.user.empleado
            entrada.precio_pagado = entrada.tipo_entrada.precio

            entrada.metodo_pago = request.POST.get('metodo_pago_1')
            metodo_pago_2 = request.POST.get('metodo_pago_2')
            monto_2 = request.POST.get('monto_2')
            if metodo_pago_2 and monto_2:
                entrada.metodo_pago_2 = metodo_pago_2
                entrada.monto_2 = Decimal(monto_2)

            entrada.save()
            messages.success(request, f'Entrada registrada: {entrada.cliente} - ${entrada.precio_pagado}')
            return redirect('registrar_entrada')
    else:
        form = EntradaDiariaForm()

    precios = {
        str(tipo.id): str(tipo.precio)
        for tipo in TipoEntrada.objects.filter(activo=True)
    }

    return render(request, 'entradas_diarias/registrar_entrada.html', {
        'form': form,
        'precios_json': json.dumps(precios),
    })