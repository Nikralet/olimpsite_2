# Generated by Django 5.0.1 on 2024-03-04 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0018_order_total_cost'),
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
            field=models.DateTimeField(verbose_name='Время доставки'),
        ),
    ]