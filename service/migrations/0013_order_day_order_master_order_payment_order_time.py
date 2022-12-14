# Generated by Django 4.0.1 on 2022-12-17 09:20

from django.db import migrations, models
import django.db.models.deletion

def filling_master(apps, schema_editor):
    Timeslot = apps.get_model('service', 'Timeslot')
    Order = apps.get_model('service', 'Order')
    for timeslot in Timeslot.objects.all().iterator():
        order = Order.objects.get(id=timeslot.id)
        order.master = timeslot.master
        order.day = timeslot.day
        order.time = timeslot.time
        order.save()

class Migration(migrations.Migration):

    dependencies = [
        ('service', '0012_alter_user_first_name_alter_user_second_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='day',
            field=models.DateField(blank=True, null=True, verbose_name='Дата записи'),
        ),
        migrations.AddField(
            model_name='order',
            name='master',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='service.master', verbose_name='Мастер'),
        ),
        migrations.AddField(
            model_name='order',
            name='payment',
            field=models.BooleanField(default=False, verbose_name='Оплата'),
        ),
        migrations.AddField(
            model_name='order',
            name='time',
            field=models.TimeField(blank=True, null=True, verbose_name='Время записи'),
        ),
        migrations.RunPython(filling_master)
    ]
