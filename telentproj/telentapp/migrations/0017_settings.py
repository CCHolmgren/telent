# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-20 12:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telentapp', '0016_userreport'),
    ]

    operations = [
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('allow_signup', models.BooleanField(default=True)),
            ],
        ),
    ]