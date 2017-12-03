# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-29 01:28
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('aggregator', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studioentry',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2016, 3, 29, 1, 28, 55, 256046, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='studioentry',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2016, 3, 29, 1, 28, 55, 255812, tzinfo=utc)),
        ),
    ]
