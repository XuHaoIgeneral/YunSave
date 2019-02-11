# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='USER',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('username', models.CharField(max_length=100)),
                ('passwd', models.CharField(max_length=255)),
                ('u_time', models.DateField(auto_now_add=True)),
            ],
            options={
                'ordering': ('-id',),
                'db_table': 'user',
            },
        ),
        migrations.AlterUniqueTogether(
            name='user',
            unique_together=set([('username',)]),
        ),
        migrations.AlterIndexTogether(
            name='user',
            index_together=set([('id', 'username')]),
        ),
    ]
