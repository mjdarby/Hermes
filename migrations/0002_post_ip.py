# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hermes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='ip',
            field=models.CharField(null=True, max_length=45),
            preserve_default=True,
        ),
    ]
