# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hermes', '0010_auto_20150228_1509'),
    ]

    operations = [
        migrations.AddField(
            model_name='thread',
            name='display_id',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='board',
            name='latest_post',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
