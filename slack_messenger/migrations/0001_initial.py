# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('git', '0002_push_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='SlackAlert',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('channel', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SlackBot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('token', models.CharField(max_length=100)),
                ('repositories', models.ManyToManyField(to='git.Repository')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='slackalert',
            name='bot',
            field=models.ForeignKey(to='slack_messenger.SlackBot'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='slackalert',
            name='branch',
            field=models.ForeignKey(to='git.Branch', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='slackalert',
            name='repository',
            field=models.ForeignKey(to='git.Repository'),
            preserve_default=True,
        ),
    ]
