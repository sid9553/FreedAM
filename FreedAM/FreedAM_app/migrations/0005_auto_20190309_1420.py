# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-03-09 14:20
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FreedAM_app', '0004_auto_20190308_1657'),
    ]

    operations = [
        migrations.AddField(
            model_name='accessories',
            name='cushion_type',
            field=models.CharField(default='1', max_length=16),
        ),
        migrations.AlterField(
            model_name='accessories',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 9, 14, 20, 39, 684000)),
        ),
        migrations.AlterField(
            model_name='contact',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 9, 14, 20, 39, 660000)),
        ),
        migrations.AlterField(
            model_name='framedimensions',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 9, 14, 20, 39, 684000)),
        ),
    ]