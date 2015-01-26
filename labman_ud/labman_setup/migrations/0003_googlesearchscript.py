# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from redactor.fields import RedactorField


class Migration(migrations.Migration):

    dependencies = [
        ('labman_setup', '0002_twittercardsconfiguration'),
    ]

    operations = [
        migrations.AddField(
            model_name='labmandeploygeneralsettings',
            name='google_search_script',
            field=RedactorField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
