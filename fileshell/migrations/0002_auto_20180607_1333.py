# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-07 13:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fileshell', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='localPath',
        ),
        migrations.AlterField(
            model_name='file',
            name='last_view_TM',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]