# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('git_scheduler', '0006_auto_20151008_2358'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='githubaccesstoken',
            name='submit_status',
        ),
        migrations.AddField(
            model_name='tasktopush',
            name='submit_status',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
