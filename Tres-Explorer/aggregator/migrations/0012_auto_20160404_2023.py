# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-04 20:23
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('aggregator', '0011_auto_20160404_1811'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studioentry',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 4, 20, 23, 8, 903080, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='studioentry',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 4, 20, 23, 8, 902851, tzinfo=utc)),
        ),
    ]
