# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hermes', '0009_board_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='latest_post',
            field=models.IntegerField(default=1),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='board',
            field=models.ForeignKey(to='hermes.Board', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='post_id',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='post',
            unique_together=set([('post_id', 'board')]),
        ),
    ]
