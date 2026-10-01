from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import datetime, time
from django.utils import timezone

from ventas_planes.models import VentaPlan
from entradas_diarias.models import EntradaDiaria
from ventas_productos.models import Venta, Pago
from egresos.models import Egreso


@login_required
def inicio(request):
    return render(request, 'inicio.html')


@login_required
def reporte_ventas(request):
    fecha_desde_str = request.GET.get('fecha_desde')
    fecha_hasta_str = request.GET.get('fecha_hasta')

    if fecha_desde_str:
        fecha_desde = datetime.strptime(fecha_desde_str, '%Y-%m-%d').date()
    else:
        fecha_desde = timezone.now().date()

    if fecha_hasta_str:
        fecha_hasta = datetime.strptime(fecha_hasta_str, '%Y-%m-%d').date()
    else:
        fecha_hasta = timezone.now().date()

    inicio_dt = datetime.combine(fecha_desde, time.min)
    fin_dt = datetime.combine(fecha_hasta, time.max)
    if timezone.is_aware(timezone.now()):
        inicio_dt = timezone.make_aware(inicio_dt)
        fin_dt = timezone.make_aware(fin_dt)

    modulo = request.GET.get('modulo', 'todos')

    movimientos = []

    if modulo in ('todos', 'planes'):
        for v in VentaPlan.objects.filter(fecha_venta__range=(inicio_dt, fin_dt)):
            pagos = []
            if v.metodo_pago_2 and v.monto_2:
                monto_1 = v.precio_pagado - v.monto_2
                pagos.append({'metodo': v.metodo_pago, 'monto': monto_1})
                pagos.append({'metodo': v.metodo_pago_2, 'monto': v.monto_2})
            else:
                pagos.append({'metodo': v.metodo_pago, 'monto': v.precio_pagado})
            movimientos.append({
                'modulo': 'Plan',
                'modulo_url': 'plan',
                'id': v.id,
                'cliente': str(v.cliente),
                'detalle': str(v.plan),
                'pagos': pagos,
                'total': v.precio_pagado,
                'fecha': v.fecha_venta,
            })

    if modulo in ('todos', 'entradas'):
        for e in EntradaDiaria.objects.filter(fecha__range=(inicio_dt, fin_dt)):
            pagos = []
            if e.metodo_pago_2 and e.monto_2:
                monto_1 = e.precio_pagado - e.monto_2
                pagos.append({'metodo': e.metodo_pago, 'monto': monto_1})
                pagos.append({'metodo': e.metodo_pago_2, 'monto': e.monto_2})
            else:
                pagos.append({'metodo': e.metodo_pago, 'monto': e.precio_pagado})
            movimientos.append({
                'modulo': 'Entrada',
                'modulo_url': 'entrada',
                'id': e.id,
                'cliente': str(e.cliente),
                'detalle': str(e.tipo_entrada),
                'pagos': pagos,
                'total': e.precio_pagado,
                'fecha': e.fecha,
            })

    if modulo in ('todos', 'productos'):
        ventas = Venta.objects.filter(fecha__range=(inicio_dt, fin_dt)).select_related('cliente').prefetch_related('items__producto', 'pagos')
        for venta in ventas:
            items = list(venta.items.all())
            if len(items) == 1:
                detalle = f'{items[0].producto.nombre} x{items[0].cantidad}'
            else:
                detalle = f'{len(items)} productos'
            pagos = [{'metodo': p.metodo_pago, 'monto': p.monto} for p in venta.pagos.all()]
            total = sum(p.monto for p in venta.pagos.all())
            movimientos.append({
                'modulo': 'Producto',
                'modulo_url': 'producto',
                'id': venta.id,
                'cliente': str(venta.cliente),
                'detalle': detalle,
                'pagos': pagos,
                'total': total,
                'fecha': venta.fecha,
            })

    movimientos.sort(key=lambda m: (m['fecha'], m['id']), reverse=True)

    total_efectivo = 0
    total_transferencia = 0
    for m in movimientos:
        for p in m['pagos']:
            if p['metodo'].lower() == 'efectivo':
                total_efectivo += p['monto']
            else:
                total_transferencia += p['monto']
    total_ventas = total_efectivo + total_transferencia

    context = {
        'fecha_desde': fecha_desde,
        'fecha_hasta': fecha_hasta,
        'modulo': modulo,
        'movimientos': movimientos,
        'total_efectivo': total_efectivo,
        'total_transferencia': total_transferencia,
        'total_ventas': total_ventas,
    }
    return render(request, 'reporte_ventas.html', context)


@login_required
def ticket_detalle(request, modulo, id):
    if modulo == 'plan':
        v = VentaPlan.objects.get(id=id)
        items = [{'nombre': str(v.plan), 'cantidad': 1, 'subtotal': v.precio_pagado}]
        pagos = []
        if v.metodo_pago_2 and v.monto_2:
            pagos.append({'metodo': v.metodo_pago, 'monto': v.precio_pagado - v.monto_2})
            pagos.append({'metodo': v.metodo_pago_2, 'monto': v.monto_2})
        else:
            pagos.append({'metodo': v.metodo_pago, 'monto': v.precio_pagado})
        cliente = v.cliente
        fecha = v.fecha_venta
        total = v.precio_pagado
    elif modulo == 'entrada':
        e = EntradaDiaria.objects.get(id=id)
        items = [{'nombre': str(e.tipo_entrada), 'cantidad': 1, 'subtotal': e.precio_pagado}]
        pagos = []
        if e.metodo_pago_2 and e.monto_2:
            pagos.append({'metodo': e.metodo_pago, 'monto': e.precio_pagado - e.monto_2})
            pagos.append({'metodo': e.metodo_pago_2, 'monto': e.monto_2})
        else:
            pagos.append({'metodo': e.metodo_pago, 'monto': e.precio_pagado})
        cliente = e.cliente
        fecha = e.fecha
        total = e.precio_pagado
    else:
        venta = Venta.objects.get(id=id)
        items = [{'nombre': i.producto.nombre, 'cantidad': i.cantidad, 'subtotal': i.precio_pagado} for i in venta.items.all()]
        pagos = [{'metodo': p.metodo_pago, 'monto': p.monto} for p in venta.pagos.all()]
        cliente = venta.cliente
        fecha = venta.fecha
        total = sum(p['monto'] for p in pagos)
    context = {'modulo': modulo, 'id': id, 'cliente': cliente, 'fecha': fecha, 'items': items, 'pagos': pagos, 'total': total}
    return render(request, 'ticket.html', context)


@login_required
def caja(request):
    fecha_desde_str = request.GET.get('fecha_desde')
    fecha_hasta_str = request.GET.get('fecha_hasta')

    if fecha_desde_str:
        fecha_desde = datetime.strptime(fecha_desde_str, '%Y-%m-%d').date()
    else:
        fecha_desde = timezone.now().date()

    if fecha_hasta_str:
        fecha_hasta = datetime.strptime(fecha_hasta_str, '%Y-%m-%d').date()
    else:
        fecha_hasta = timezone.now().date()

    inicio_dt = datetime.combine(fecha_desde, time.min)
    fin_dt = datetime.combine(fecha_hasta, time.max)
    if timezone.is_aware(timezone.now()):
        inicio_dt = timezone.make_aware(inicio_dt)
        fin_dt = timezone.make_aware(fin_dt)

    ingresos_efectivo = 0
    ingresos_transferencia = 0

    for v in VentaPlan.objects.filter(fecha_venta__range=(inicio_dt, fin_dt)):
        if v.metodo_pago_2 and v.monto_2:
            monto_1 = v.precio_pagado - v.monto_2
            if v.metodo_pago.lower() == 'efectivo':
                ingresos_efectivo += monto_1
            else:
                ingresos_transferencia += monto_1
            if v.metodo_pago_2.lower() == 'efectivo':
                ingresos_efectivo += v.monto_2
            else:
                ingresos_transferencia += v.monto_2
        else:
            if v.metodo_pago.lower() == 'efectivo':
                ingresos_efectivo += v.precio_pagado
            else:
                ingresos_transferencia += v.precio_pagado

    for e in EntradaDiaria.objects.filter(fecha__range=(inicio_dt, fin_dt)):
        if e.metodo_pago_2 and e.monto_2:
            monto_1 = e.precio_pagado - e.monto_2
            if e.metodo_pago.lower() == 'efectivo':
                ingresos_efectivo += monto_1
            else:
                ingresos_transferencia += monto_1
            if e.metodo_pago_2.lower() == 'efectivo':
                ingresos_efectivo += e.monto_2
            else:
                ingresos_transferencia += e.monto_2
        else:
            if e.metodo_pago.lower() == 'efectivo':
                ingresos_efectivo += e.precio_pagado
            else:
                ingresos_transferencia += e.precio_pagado

    for pago in Pago.objects.filter(venta__fecha__range=(inicio_dt, fin_dt)):
        if pago.metodo_pago.lower() == 'efectivo':
            ingresos_efectivo += pago.monto
        else:
            ingresos_transferencia += pago.monto

    total_ingresos = ingresos_efectivo + ingresos_transferencia

    egresos_efectivo = 0
    egresos_transferencia = 0

    for eg in Egreso.objects.filter(fecha__range=(fecha_desde, fecha_hasta)):
        if eg.metodo_pago.lower() == 'efectivo':
            egresos_efectivo += eg.monto
        else:
            egresos_transferencia += eg.monto

    total_egresos = egresos_efectivo + egresos_transferencia

    neto_efectivo = ingresos_efectivo - egresos_efectivo
    neto_transferencia = ingresos_transferencia - egresos_transferencia
    neto_total = neto_efectivo + neto_transferencia

    context = {
        'fecha_desde': fecha_desde,
        'fecha_hasta': fecha_hasta,
        'ingresos_efectivo': ingresos_efectivo,
        'ingresos_transferencia': ingresos_transferencia,
        'total_ingresos': total_ingresos,
        'egresos_efectivo': egresos_efectivo,
        'egresos_transferencia': egresos_transferencia,
        'total_egresos': total_egresos,
        'neto_efectivo': neto_efectivo,
        'neto_transferencia': neto_transferencia,
        'neto_total': neto_total,
    }
    return render(request, 'caja.html', context)