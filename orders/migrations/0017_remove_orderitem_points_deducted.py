# Generated by Django 5.0.1 on 2024-03-02 21:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0016_remove_order_points_deducted_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='points_deducted',
        ),
    ]