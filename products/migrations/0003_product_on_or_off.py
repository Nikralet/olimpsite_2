# Generated by Django 5.0.1 on 2024-03-04 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='on_or_off',
            field=models.BooleanField(default=True, verbose_name='Включить'),
        ),
    ]