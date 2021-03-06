# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-31 17:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_auto_20170330_2153'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sale',
            name='product',
        ),
        migrations.RemoveField(
            model_name='sale',
            name='tax',
        ),
        migrations.AddField(
            model_name='rentalproduct',
            name='available',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='sale',
            name='shippping',
            field=models.DecimalField(decimal_places=2, default=10, max_digits=8),
        ),
        migrations.AddField(
            model_name='saleitem',
            name='taxamount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='saleitem',
            name='taxrate',
            field=models.DecimalField(decimal_places=2, default=0.0725, max_digits=8),
        ),
        migrations.AddField(
            model_name='uniqueproduct',
            name='available',
            field=models.BooleanField(default=True),
        ),
    ]
