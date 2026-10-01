from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from datetime import timedelta
from decimal import Decimal
from dateutil.relativedelta import relativedelta
from django.http import JsonResponse
from django.contrib import messages
import json

from .forms import VentaPlanForm
from .models import VentaPlan
from planes.models import Plan


@login_required
def registrar_venta_plan(request):
    if request.method == 'POST':
        form = VentaPlanForm(request.POST)
        if form.is_valid():
            venta = form.save(commit=False)
            venta.empleado = request.user.empleado
            venta.precio_pagado = venta.plan.precio

            if venta.plan.unidad_duracion == 'meses':
                venta.fecha_vencimiento = venta.fecha_inicio + relativedelta(months=venta.plan.duracion)
            else:
                venta.fecha_vencimiento = venta.fecha_inicio + timedelta(days=venta.plan.duracion)

            venta.metodo_pago = request.POST.get('metodo_pago_1')
            metodo_pago_2 = request.POST.get('metodo_pago_2')
            monto_2 = request.POST.get('monto_2')
            if metodo_pago_2 and monto_2:
                venta.metodo_pago_2 = metodo_pago_2
                venta.monto_2 = Decimal(monto_2)

            venta.save()
            messages.success(request, f'Venta de plan registrada: {venta.cliente} - {venta.plan.nombre} - ${venta.precio_pagado}')
            return redirect('registrar_venta_plan')
    else:
        form = VentaPlanForm()

    planes_json = json.dumps({str(p.id): str(p.precio) for p in Plan.objects.all()})
    return render(request, 'ventas_planes/registrar_venta_plan.html', {'form': form, 'planes_json': planes_json})


@login_required
def ultimo_plan_cliente(request, cliente_id):
    ultima_venta = VentaPlan.objects.filter(cliente_id=cliente_id).order_by('-fecha_vencimiento').first()

    if ultima_venta:
        datos = {
            'existe': True,
            'plan': ultima_venta.plan.nombre,
            'fecha_inicio': ultima_venta.fecha_inicio.strftime('%d/%m/%Y'),
            'fecha_vencimiento': ultima_venta.fecha_vencimiento.strftime('%d/%m/%Y'),
        }
    else:
        datos = {'existe': False}

    return JsonResponse(datos)