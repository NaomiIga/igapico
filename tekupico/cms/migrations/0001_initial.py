# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-17 06:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userdata', models.CharField(default='NAME', max_length=255, verbose_name='username')),
                ('datavalue', models.FloatField(default='DATA', max_length=255, verbose_name='value')),
            ],
        ),
    ]
