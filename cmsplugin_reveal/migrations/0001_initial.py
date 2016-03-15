# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0013_urlconfrevision'),
    ]

    operations = [
        migrations.CreateModel(
            name='RevealExtension',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('options', jsonfield.fields.JSONField(default={}, blank=True)),
                ('extended_object', models.OneToOneField(editable=False, to='cms.Page')),
                ('public_extension', models.OneToOneField(related_name='draft_extension', null=True, editable=False, to='cmsplugin_reveal.RevealExtension')),
            ],
            options={
                'db_table': 'cmsplugin_cascade_reveal',
                'verbose_name': 'Reveal Option',
                'verbose_name_plural': 'Reveal Options',
            },
        ),
    ]
