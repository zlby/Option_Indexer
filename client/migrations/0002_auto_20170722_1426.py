# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='notificationhistory',
            options={'ordering': ['-time']},
        ),
        migrations.AddField(
            model_name='notificationhistory',
            name='if_read',
            field=models.BooleanField(verbose_name='是否已读', default=False),
        ),
    ]
