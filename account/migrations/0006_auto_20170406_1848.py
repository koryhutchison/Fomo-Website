# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-06 18:48
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_remove_shippingaddress_sale'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shippingaddress',
            name='user',
        ),
        migrations.DeleteModel(
            name='ShippingAddress',
        ),
    ]
