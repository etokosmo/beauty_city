# Generated by Django 4.1 on 2022-12-15 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("service", "0004_alter_master_options_alter_salon_options_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="salon",
            name="image",
            field=models.ImageField(
                blank=True, null=True, upload_to="", verbose_name="Аватарка салона"
            ),
        ),
    ]
