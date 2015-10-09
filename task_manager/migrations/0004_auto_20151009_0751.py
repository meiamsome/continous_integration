# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task_manager', '0003_task_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scheduledtask',
            name='output',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='scheduledtask',
            name='working_directory',
            field=models.TextField(blank=True),
        ),
    ]
