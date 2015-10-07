# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task_manager', '0002_auto_20151002_1905'),
        ('git', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegisteredTask',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.CharField(max_length=32)),
                ('assign_on_push', models.BooleanField(default=False)),
                ('repository', models.ForeignKey(to='git.Repository')),
                ('task', models.ForeignKey(to='task_manager.Task')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
