# Generated by Django 5.0.3 on 2024-05-22 13:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_ordercountpast'),
    ]

    operations = [
        migrations.DeleteModel(
            name='OrderCountPast',
        ),
    ]
