# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-20 12:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telentapp', '0017_settings'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='in_limbo',
            field=models.BooleanField(default=False),
        ),
    ]