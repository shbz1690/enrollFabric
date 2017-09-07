# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinformation',
            name='ctsaPIInstitution',
            field=models.CharField(default=b'N/A', max_length=128, choices=[(b'@childrensnational.org', b"Children's National Medical Center"), (b'@gwu.edu', b'George Washington University')]),
        ),
    ]
