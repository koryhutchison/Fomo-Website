# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-28 19:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fomouser',
            name='birth_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]