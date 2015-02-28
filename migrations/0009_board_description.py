# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hermes', '0008_auto_20150228_0114'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='description',
            field=models.CharField(max_length=1000, default='Board'),
            preserve_default=True,
        ),
    ]
