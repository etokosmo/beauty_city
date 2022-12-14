# Generated by Django 4.0.1 on 2022-12-16 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0009_alter_order_options_alter_user_first_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название документа')),
                ('file', models.FileField(upload_to='', verbose_name='Файл')),
            ],
            options={
                'verbose_name': 'Документ',
                'verbose_name_plural': 'Документы',
            },
        ),
    ]
