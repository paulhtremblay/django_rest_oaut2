# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-17 03:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('henry', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotManaged',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('dob', models.DateField()),
            ],
            options={
                'db_table': 'old_dob',
                'managed': True,
            },
        ),
        migrations.AlterModelOptions(
            name='dob',
            options={'managed': True},
        ),
        migrations.AlterModelTable(
            name='dob',
            table='henry_dob',
        ),
    ]