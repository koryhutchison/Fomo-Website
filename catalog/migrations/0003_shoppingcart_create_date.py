# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-29 19:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_auto_20170328_1927'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoppingcart',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
