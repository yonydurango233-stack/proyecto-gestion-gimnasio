from django.db import migrations


def actualizar_a_minuscula(apps, schema_editor):
    Egreso = apps.get_model('egresos', 'Egreso')
    Egreso.objects.filter(metodo_pago='Efectivo').update(metodo_pago='efectivo')
    Egreso.objects.filter(metodo_pago='Transferencia').update(metodo_pago='transferencia')


def revertir_a_mayuscula(apps, schema_editor):
    Egreso = apps.get_model('egresos', 'Egreso')
    Egreso.objects.filter(metodo_pago='efectivo').update(metodo_pago='Efectivo')
    Egreso.objects.filter(metodo_pago='transferencia').update(metodo_pago='Transferencia')


class Migration(migrations.Migration):

    dependencies = [
        ('egresos', '0002_alter_egreso_metodo_pago'),
    ]

    operations = [
        migrations.RunPython(actualizar_a_minuscula, revertir_a_mayuscula),
    ]