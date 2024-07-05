# Generated by Django 5.0.3 on 2024-07-05 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_alter_product_number_of_pieces'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='min_quantity_by_weight',
            field=models.DecimalField(decimal_places=0, default=100, max_digits=8, verbose_name='Мин. кол-во по весу'),
        ),
    ]
