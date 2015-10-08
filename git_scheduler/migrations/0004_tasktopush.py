# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task_manager', '0003_task_name'),
        ('git', '0002_push_time'),
        ('git_scheduler', '0003_registeredtask_working_directory'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskToPush',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('push', models.ForeignKey(to='git.Push')),
                ('task', models.ForeignKey(to='task_manager.Task')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
