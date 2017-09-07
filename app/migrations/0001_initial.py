# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserInformation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('firstName', models.CharField(max_length=128)),
                ('lastName', models.CharField(max_length=128)),
                ('username', models.CharField(max_length=128)),
                ('institution', models.CharField(max_length=128, choices=[(b"Children's National Medical Center", b'@childrensnational.org'), (b'George Washington University', b'@gwu.edu')])),
                ('phoneNumber', models.CharField(max_length=128)),
                ('orchidNumber', models.CharField(max_length=128)),
                ('cstaPI', models.CharField(max_length=128)),
                ('cstaPIUsername', models.CharField(max_length=128)),
                ('ctsaPIPhoneNumber', models.CharField(max_length=128)),
            ],
        ),
    ]
