# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-06 18:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_shippingaddress'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shippingaddress',
            name='sale',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shippingaddress', to='catalog.Sale'),
        ),
    ]
