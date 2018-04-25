# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-04-25 18:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0003_quote_quotedby'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quote',
            name='liked_users',
            field=models.ManyToManyField(related_name='liked_quotes', to='first_app.User'),
        ),
    ]
