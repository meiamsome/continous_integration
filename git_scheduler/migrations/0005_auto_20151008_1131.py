# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('git_scheduler', '0004_tasktopush'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasktopush',
            name='task',
            field=models.ForeignKey(to='task_manager.ScheduledTask'),
        ),
    ]
