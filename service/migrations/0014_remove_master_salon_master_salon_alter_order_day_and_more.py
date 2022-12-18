# Generated by Django 4.0.1 on 2022-12-18 08:37

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0013_order_day_order_master_order_payment_order_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='master',
            name='salon',
        ),
        migrations.AddField(
            model_name='master',
            name='salon',
            field=models.ManyToManyField(null=True, related_name='masters', to='service.Salon', verbose_name='Салон'),
        ),
        migrations.AlterField(
            model_name='order',
            name='day',
            field=models.DateField(verbose_name='Дата записи'),
        ),
        migrations.AlterField(
            model_name='order',
            name='master',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.master', verbose_name='Мастер'),
        ),
        migrations.AlterField(
            model_name='order',
            name='time',
            field=models.TimeField(default=django.utils.timezone.now, verbose_name='Время записи'),
            preserve_default=False,
        ),
    ]