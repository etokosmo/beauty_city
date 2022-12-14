# Generated by Django 4.0.1 on 2022-12-16 13:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0010_document'),
    ]

    operations = [
        migrations.AddField(
            model_name='salon',
            name='categories',
            field=models.ManyToManyField(related_name='salons', to='service.ServiceCategory', verbose_name='Категории салона'),
        ),
        migrations.AddField(
            model_name='service',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='Аватарка салона'),
        ),
        migrations.AlterField(
            model_name='master',
            name='salon',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='masters', to='service.salon'),
        ),
    ]
