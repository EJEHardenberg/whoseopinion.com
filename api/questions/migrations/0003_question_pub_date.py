# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0002_auto_20140908_2029'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='pub_date',
            field=models.DateTimeField(default=datetime.date(2014, 9, 8), verbose_name=b'date published'),
            preserve_default=False,
        ),
    ]
