# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ScheduledTasks',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('arguments', models.TextField()),
                ('user', models.CharField(max_length=32, null=True)),
                ('status', models.SmallIntegerField(choices=[(1, b'Completed'), (0, b'Queued'), (-1, b'Error')])),
                ('working_directory', models.TextField()),
                ('output', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('execution', models.TextField()),
                ('is_safe', models.BooleanField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='scheduledtasks',
            name='task',
            field=models.ForeignKey(to='task_manager.Task'),
            preserve_default=True,
        ),
    ]
