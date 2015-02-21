# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hermes', '0004_post_admin_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='tripcode',
            field=models.CharField(null=True, max_length=30),
            preserve_default=True,
        ),
    ]
