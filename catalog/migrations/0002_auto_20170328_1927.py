# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-28 19:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='saleitem',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='shoppingcart',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]