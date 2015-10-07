# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('git', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='push',
            name='time',
            field=models.DateTimeField(default=datetime.date(2015, 10, 6)),
            preserve_default=False,
        ),
    ]
