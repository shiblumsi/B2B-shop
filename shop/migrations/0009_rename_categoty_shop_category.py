# Generated by Django 4.2.2 on 2023-07-11 13:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_alter_cartitem_cart'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shop',
            old_name='categoty',
            new_name='category',
        ),
    ]