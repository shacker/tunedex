# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-04-29 06:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itl', '0002_track_loved'),
    ]

    operations = [
        migrations.AddField(
            model_name='track',
            name='persistent_id',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]