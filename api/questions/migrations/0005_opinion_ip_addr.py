# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0004_auto_20140909_1658'),
    ]

    operations = [
        migrations.AddField(
            model_name='opinion',
            name='ip_addr',
            field=models.CharField(default=b'127.0.0.1', max_length=64),
            preserve_default=True,
        ),
    ]
