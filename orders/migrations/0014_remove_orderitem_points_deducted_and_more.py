# Generated by Django 5.0.1 on 2024-03-02 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0013_orderitem_points_deducted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='points_deducted',
        ),
        migrations.AddField(
            model_name='order',
            name='points_deducted',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=8, verbose_name='Списано баллов'),
        ),
    ]