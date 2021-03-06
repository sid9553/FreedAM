# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-02-08 16:22
from __future__ import unicode_literals

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_date', models.DateTimeField(default=datetime.datetime(2019, 2, 8, 16, 22, 17, 440000))),
                ('name', models.CharField(max_length=50)),
                ('email_address', models.EmailField(max_length=254)),
                ('query', models.CharField(max_length=250)),
            ],
            options={
                'verbose_name': 'Contact forms received',
            },
        ),
        migrations.CreateModel(
            name='FrameDimensions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_date', models.DateTimeField(default=datetime.datetime(2019, 2, 8, 16, 22, 17, 458000))),
                ('angle_lower_leg_upper_leg', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('backrest_angle', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('seating_angle', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('seat_width', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('seat_depth', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('seat_height', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('backrest_height', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
            ],
            options={
                'verbose_name': 'Frame dimensions',
            },
        ),
    ]
