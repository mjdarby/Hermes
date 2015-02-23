# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hermes', '0005_post_tripcode'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='recaptcha_enabled',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
