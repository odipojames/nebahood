# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2019-01-10 22:23
from __future__ import unicode_literals

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=tinymce.models.HTMLField(default='majiriani wema'),
        ),
    ]