# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('git_scheduler', '0002_registeredtask_branch'),
    ]

    operations = [
        migrations.AddField(
            model_name='registeredtask',
            name='working_directory',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
