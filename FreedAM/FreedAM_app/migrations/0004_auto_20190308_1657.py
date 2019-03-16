# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-03-08 16:57
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('FreedAM_app', '0003_auto_20190227_1919'),
    ]

    operations = [
        migrations.CreateModel(
            name='Accessories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_date', models.DateTimeField(default=datetime.datetime(2019, 3, 8, 16, 57, 2, 181000))),
            ],
            options={
                'verbose_name': 'Chair Accessories',
            },
        ),
        migrations.AlterField(
            model_name='contact',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 8, 16, 57, 2, 156000)),
        ),
        migrations.AlterField(
            model_name='framedimensions',
            name='angle_lower_leg_upper_leg',
            field=models.IntegerField(verbose_name='Angle of footrest position to seat'),
        ),
        migrations.AlterField(
            model_name='framedimensions',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 8, 16, 57, 2, 180000)),
        ),
        migrations.AddField(
            model_name='accessories',
            name='linked_frame',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FreedAM_app.FrameDimensions'),
        ),
    ]