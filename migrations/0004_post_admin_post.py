# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hermes', '0003_ban'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='admin_post',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
