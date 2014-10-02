# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0005_opinion_ip_addr'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opinion',
            name='ip_addr',
            field=models.CharField(default=b'127.0.0.1', max_length=64, null=True, blank=True),
        ),
    ]
