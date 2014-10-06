# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0006_auto_20141002_1355'),
    ]

    operations = [
        migrations.AddField(
            model_name='opinion',
            name='country_code',
            field=models.CharField(default='US', max_length=8),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='opinion',
            name='region',
            field=models.CharField(default='CA', max_length=8),
            preserve_default=False,
        ),
    ]
