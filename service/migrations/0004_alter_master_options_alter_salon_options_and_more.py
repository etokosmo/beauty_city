# Generated by Django 4.0.1 on 2022-12-14 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0003_order'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='master',
            options={'verbose_name': 'Мастер', 'verbose_name_plural': 'Мастера'},
        ),
        migrations.AlterModelOptions(
            name='salon',
            options={'verbose_name': 'Салон', 'verbose_name_plural': 'Салоны'},
        ),
        migrations.AlterModelOptions(
            name='service',
            options={'verbose_name': 'Услуга', 'verbose_name_plural': 'Услуги'},
        ),
        migrations.AlterModelOptions(
            name='servicecategory',
            options={'verbose_name': 'Категория услуги', 'verbose_name_plural': 'Категории услуг'},
        ),
        migrations.AlterModelOptions(
            name='timeslot',
            options={'verbose_name': 'Запись', 'verbose_name_plural': 'Записи'},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
        migrations.AddField(
            model_name='master',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='Аватарка'),
        ),
        migrations.AddField(
            model_name='user',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='Аватарка'),
        ),
        migrations.AddField(
            model_name='user',
            name='passcode',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Код проверки'),
        ),
        migrations.AlterField(
            model_name='master',
            name='service',
            field=models.ManyToManyField(related_name='masters', to='service.Service', verbose_name='Услуги мастера'),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Имя клиента'),
        ),
        migrations.AlterField(
            model_name='user',
            name='second_name',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Фамилия клиента'),
        ),
    ]
