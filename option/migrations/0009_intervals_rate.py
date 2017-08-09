# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('option', '0008_dayfuturetreadingdata_dayoptiontreadingdata_hourfuturetreadingdata_houroptiontreadingdata'),
    ]

    operations = [
        migrations.AddField(
            model_name='intervals',
            name='rate',
            field=models.FloatField(default=1, verbose_name='买卖比例'),
        ),
    ]
