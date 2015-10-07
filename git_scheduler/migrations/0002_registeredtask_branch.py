# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('git', '0002_push_time'),
        ('git_scheduler', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='registeredtask',
            name='branch',
            field=models.ForeignKey(blank=True, to='git.Branch', null=True),
            preserve_default=True,
        ),
    ]
