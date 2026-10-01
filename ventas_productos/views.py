import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from decimal import Decimal

from clientes.models import Cliente
from productos.models import Producto
from empleados.models import Empleado
from .models import Venta, VentaProducto, Pago


@login_required
def registrar_venta_producto(request):
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente_id')
        carrito_json = request.POST.get('carrito_json')
        metodo_pago_1 = request.POST.get('metodo_pago_1')
        monto_1 = request.POST.get('monto_1')
        metodo_pago_2 = request.POST.get('metodo_pago_2')
        monto_2 = request.POST.get('monto_2')

        try:
            carrito = json.loads(carrito_json)
        except (TypeError, ValueError):
            carrito = []

        if not cliente_id or not carrito:
            messages.error(request, 'Elegí un cliente y agregá al menos un producto.')
            return redirect('registrar_venta_producto')

        cliente = Cliente.objects.get(id=cliente_id)
        empleado = Empleado.objects.get(usuario=request.user)

        # Validar stock de todo el carrito antes de guardar nada
        for item in carrito:
            producto = Producto.objects.get(id=item['producto_id'])
            if item['cantidad'] > producto.stock:
                messages.error(request, f'No hay suficiente stock de {producto.nombre}.')
                return redirect('registrar_venta_producto')

        # Crear la venta (cabecera)
        venta = Venta.objects.create(cliente=cliente, empleado=empleado)

        total_venta = Decimal('0')
        detalle_texto = []

        for item in carrito:
            producto = Producto.objects.get(id=item['producto_id'])
            cantidad = item['cantidad']
            precio_linea = producto.precio * cantidad

            VentaProducto.objects.create(
                venta=venta,
                producto=producto,
                cantidad=cantidad,
                precio_pagado=precio_linea,
            )

            producto.stock -= cantidad
            producto.save()

            total_venta += precio_linea
            detalle_texto.append(f'{producto.nombre} x{cantidad}')

        # Registrar el/los pagos
        Pago.objects.create(venta=venta, metodo_pago=metodo_pago_1, monto=Decimal(monto_1))
        if metodo_pago_2 and monto_2:
            Pago.objects.create(venta=venta, metodo_pago=metodo_pago_2, monto=Decimal(monto_2))

        messages.success(request, f'Venta registrada: {cliente} - {", ".join(detalle_texto)} - ${total_venta}')
        return redirect('registrar_venta_producto')

    # GET: mostrar la pantalla
    productos = Producto.objects.filter(activo=True)
    clientes = Cliente.objects.filter(activo=True)
    cliente_predeterminado = Cliente.objects.filter(numero_documento='00000000').first()

    productos_json = json.dumps([
    {
        'id': p.id,
        'nombre': p.nombre,
        'precio': str(p.precio),
        'categoria': p.categoria,
        'imagen': p.imagen.url if p.imagen else None,
    }
    for p in productos
])

    context = {
        'productos': productos,
        'clientes': clientes,
        'productos_json': productos_json,
        'cliente_predeterminado_id': cliente_predeterminado.id if cliente_predeterminado else None,
    }
    return render(request, 'ventas_productos/registrar_venta_producto.html', context)