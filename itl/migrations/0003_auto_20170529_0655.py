# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-29 06:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itl', '0002_album_album_loved'),
    ]

    operations = [
        migrations.AddField(
            model_name='librarydata',
            name='facebook',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='librarydata',
            name='twitter',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
