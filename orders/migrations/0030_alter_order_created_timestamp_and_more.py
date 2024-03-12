# Generated by Django 5.0.1 on 2024-03-12 13:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0029_alter_order_created_timestamp_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='created_timestamp',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='Дата создания заказа'),
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery_datetime',
            field=models.DateTimeField(default=datetime.datetime.now, null=True, verbose_name='Дата-время доставки'),
        ),
    ]