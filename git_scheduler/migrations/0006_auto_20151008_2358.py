# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('git', '0002_push_time'),
        ('git_scheduler', '0005_auto_20151008_1131'),
    ]

    operations = [
        migrations.CreateModel(
            name='GitHubAccessToken',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('token', models.CharField(max_length=40)),
                ('submit_status', models.BooleanField(default=False)),
                ('repositories', models.ManyToManyField(to='git.Repository')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='registeredtask',
            name='submit_status',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
