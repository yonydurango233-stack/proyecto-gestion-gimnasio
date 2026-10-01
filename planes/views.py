from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Plan
from .forms import PlanForm


@login_required
def listar_planes(request):
    planes = Plan.objects.all().order_by('nombre')
    return render(request, 'planes/listar_planes.html', {'planes': planes})


@login_required
def crear_plan(request):
    if request.method == 'POST':
        form = PlanForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Plan creado correctamente.')
            return redirect('listar_planes')
    else:
        form = PlanForm()

    return render(request, 'planes/form_plan.html', {'form': form, 'titulo': 'Crear plan'})


@login_required
def editar_plan(request, plan_id):
    plan = get_object_or_404(Plan, id=plan_id)

    if request.method == 'POST':
        form = PlanForm(request.POST, instance=plan)
        if form.is_valid():
            form.save()
            messages.success(request, 'Plan actualizado correctamente.')
            return redirect('listar_planes')
    else:
        form = PlanForm(instance=plan)

    return render(request, 'planes/form_plan.html', {'form': form, 'titulo': 'Editar plan'})