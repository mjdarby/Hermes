# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hermes', '0006_board_recaptcha_enabled'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='short_name',
            field=models.CharField(default='gen', max_length=50),
            preserve_default=True,
        ),
    ]
