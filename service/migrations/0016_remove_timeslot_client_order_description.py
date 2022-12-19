# Generated by Django 4.0.1 on 2022-12-19 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0015_alter_master_salon'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timeslot',
            name='client',
        ),
        migrations.AddField(
            model_name='order',
            name='description',
            field=models.TextField(blank=True, verbose_name='Вопрос к заказу'),
        ),
    ]
