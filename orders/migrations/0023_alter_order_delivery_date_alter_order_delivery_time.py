# Generated by Django 5.0.1 on 2024-03-04 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0022_alter_order_created_timestamp_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivery_date',
            field=models.DateField(verbose_name='Дата доставки'),
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery_time',
            field=models.TimeField(verbose_name='Время доставки'),
        ),
    ]
