# Generated by Django 5.0.1 on 2024-03-13 15:44

import phonenumber_field.modelfields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания заказа')),
                ('delivery_datetime', models.DateTimeField(null=True, verbose_name='Дата-время доставки')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None, verbose_name='Номер телефона')),
                ('requires_delivery', models.BooleanField(default=False, verbose_name='Требуется доставка')),
                ('delivery_address', models.TextField(blank=True, null=True, verbose_name='Адрес доставки')),
                ('payment_on_get', models.BooleanField(default=False, verbose_name='Оплата при получении')),
                ('is_paid', models.BooleanField(default=False, verbose_name='Оплачено')),
                ('deduct_points', models.BooleanField(default=False, verbose_name='Баллы списаны')),
                ('is_add', models.BooleanField(default=False, editable=False, verbose_name='Просто функция, не трогать')),
                ('status', models.CharField(choices=[('В обработке', 'В обработке'), ('В пути', 'В пути'), ('Доставлен', 'Доставлен')], default='В обработке', max_length=50, verbose_name='Статус заказа')),
                ('total_cost', models.DecimalField(decimal_places=0, default=0, max_digits=8, verbose_name='Суммарная стоимость')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
                'db_table': 'order',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Название')),
                ('price', models.DecimalField(decimal_places=0, max_digits=8, verbose_name='Цена')),
                ('weight', models.DecimalField(decimal_places=0, max_digits=8, verbose_name='Вес')),
                ('quantity', models.PositiveIntegerField(default=0, verbose_name='Количество')),
                ('created_timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Дата продажи')),
            ],
            options={
                'verbose_name': 'Проданный товар',
                'verbose_name_plural': 'Проданные товары',
                'db_table': 'order_item',
            },
        ),
    ]
