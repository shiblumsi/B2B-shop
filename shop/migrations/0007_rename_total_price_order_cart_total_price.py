# Generated by Django 4.2.2 on 2023-06-26 18:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_order'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='total_price',
            new_name='cart_total_price',
        ),
    ]
