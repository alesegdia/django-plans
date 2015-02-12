# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plans', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='userplan',
            field=models.ForeignKey(blank=True, null=True, to='plans.UserPlan'),
            preserve_default=True,
        ),
    ]
