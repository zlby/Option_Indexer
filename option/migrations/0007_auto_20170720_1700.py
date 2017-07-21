# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('option', '0006_auto_20170719_1952'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='futuretreadingdata',
            options={'ordering': ['time']},
        ),
        migrations.AlterModelOptions(
            name='optiontreadingdata',
            options={'ordering': ['time']},
        ),
    ]
