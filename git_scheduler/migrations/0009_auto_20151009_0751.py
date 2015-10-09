# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('git_scheduler', '0008_githubaccesstoken_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registeredtask',
            name='working_directory',
            field=models.TextField(blank=True),
        ),
    ]
