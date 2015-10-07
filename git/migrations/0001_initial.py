# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ref', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Commit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hash', models.CharField(max_length=40)),
                ('previous_commit_left', models.ForeignKey(related_name=b'_next_left_set', blank=True, to='git.Commit', null=True)),
                ('previous_commit_right', models.ForeignKey(related_name=b'_next_right_set', blank=True, to='git.Commit', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Push',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('after', models.ForeignKey(related_name=b'post_pushes', to='git.Commit')),
                ('before', models.ForeignKey(related_name=b'pre_pushes', to='git.Commit')),
                ('branch', models.ForeignKey(to='git.Branch')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Repository',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('mainline', models.ForeignKey(related_name=b'__not_used', blank=True, to='git.Branch', null=True)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='push',
            name='repository',
            field=models.ForeignKey(to='git.Repository'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='commit',
            name='repository',
            field=models.ForeignKey(to='git.Repository'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='branch',
            name='head',
            field=models.ForeignKey(to='git.Commit'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='branch',
            name='repository',
            field=models.ForeignKey(to='git.Repository'),
            preserve_default=True,
        ),
    ]
