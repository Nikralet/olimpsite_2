# Generated by Django 5.0.3 on 2024-05-22 16:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_orderboolean'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderboolean',
            old_name='count',
            new_name='bool',
        ),
    ]
