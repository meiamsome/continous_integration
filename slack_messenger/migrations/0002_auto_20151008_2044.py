# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('slack_messenger', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slackalert',
            name='branch',
            field=models.ForeignKey(blank=True, to='git.Branch', null=True),
        ),
    ]
