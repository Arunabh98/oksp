# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-09 01:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('docupload', '0005_auto_20160509_0332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentation',
            name='doc_file',
            field=models.FileField(upload_to='/home/darknight/Desktop/oksp/media/'),
        ),
    ]
