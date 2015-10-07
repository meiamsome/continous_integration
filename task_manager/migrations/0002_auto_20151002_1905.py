# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task_manager', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScheduledTask',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('arguments', models.TextField()),
                ('user', models.CharField(max_length=32, null=True)),
                ('status', models.SmallIntegerField(default=0, choices=[(1, b'Completed'), (0, b'Queued'), (-1, b'Error')])),
                ('working_directory', models.TextField()),
                ('output', models.TextField()),
                ('task', models.ForeignKey(to='task_manager.Task')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='scheduledtasks',
            name='task',
        ),
        migrations.DeleteModel(
            name='ScheduledTasks',
        ),
        migrations.AlterField(
            model_name='task',
            name='is_safe',
            field=models.BooleanField(default=False),
        ),
    ]
