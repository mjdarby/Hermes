# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hermes', '0007_board_short_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='thread',
            name='autosaging',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='thread',
            name='sticky',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
