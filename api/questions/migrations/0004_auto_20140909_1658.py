# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0003_question_pub_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opinion',
            name='question',
            field=models.ForeignKey(related_name=b'opinions', to='questions.Question'),
        ),
        migrations.AlterField(
            model_name='opinion',
            name='vote',
            field=models.IntegerField(default=0, choices=[(-2, b'Strongly Disagree'), (-1, b'Disagree'), (0, b'Neutral'), (1, b'Agree'), (2, b'Strongly Agree')]),
        ),
    ]
