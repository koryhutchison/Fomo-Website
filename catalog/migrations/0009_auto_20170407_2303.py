# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-07 23:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0008_auto_20170406_1857'),
    ]

    operations = [
        migrations.AlterField(
            model_name='saleitem',
            name='taxamount',
            field=models.DecimalField(decimal_places=4, max_digits=8),
        ),
    ]
