# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('git_scheduler', '0007_auto_20151009_0001'),
    ]

    operations = [
        migrations.AddField(
            model_name='githubaccesstoken',
            name='username',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
